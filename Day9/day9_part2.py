import sys
from collections import defaultdict


def read_points(filename):
    """Read points from input file"""
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                points.append((x, y))
    return points


def get_all_valid_tiles(points):
    """
    Get all red and green tiles efficiently.
    Returns a set of (x, y) tuples.
    """
    # Store red points
    red_set = set(points)

    # Create a map for fast lookup of points at each x and y
    points_by_x = defaultdict(list)
    points_by_y = defaultdict(list)
    for x, y in points:
        points_by_x[x].append(y)
        points_by_y[y].append(x)

    # Sort for binary search
    for x in points_by_x:
        points_by_x[x].sort()
    for y in points_by_y:
        points_by_y[y].sort()

    # Get bounding box
    all_x = [x for x, _ in points]
    all_y = [y for _, y in points]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Expand slightly
    min_x -= 2
    max_x += 2
    min_y -= 2
    max_y += 2

    # Mark boundary and connections
    valid_tiles = set(red_set)
    n = len(points)

    # Add green connecting tiles
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        if x1 == x2:  # Vertical
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                valid_tiles.add((x1, y))
        else:  # Horizontal
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                valid_tiles.add((x, y1))

    # Use scanline algorithm for interior points
    # For each y, find x ranges that are inside the polygon
    for y in range(min_y, max_y + 1):
        # Find x values where vertical lines intersect this y
        intersections = []

        # Check all edges
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]

            if y1 == y2 == y:  # Horizontal edge at this y
                # Add the entire segment
                start_x, end_x = sorted([x1, x2])
                intersections.append((start_x, end_x, 'edge'))
            elif min(y1, y2) <= y <= max(y1, y2) and y1 != y2:
                # Vertical edge crossing this y
                # Calculate x at this y (linear interpolation)
                if y1 != y2:
                    # For vertical lines, x is constant
                    if x1 == x2:
                        intersections.append((x1, x1, 'cross'))
                    else:
                        # Shouldn't happen with axis-aligned edges
                        pass

        if not intersections:
            continue

        # Sort intersections
        intersections.sort()

        # Use even-odd rule to determine inside/outside
        in_polygon = False
        current_start = None

        # Process intersections
        i = 0
        while i < len(intersections):
            x_start, x_end, edge_type = intersections[i]

            if edge_type == 'edge':
                # Horizontal edge: always inside
                for x in range(x_start, x_end + 1):
                    valid_tiles.add((x, y))
                i += 1
            else:  # 'cross'
                # Count crossings
                # For vertical edges at this exact x
                x_val = x_start
                # Check if this is a local min/max
                prev_point = points[(i - 1) % n]
                next_point = points[(i + 1) % n]
                y_prev = prev_point[1]
                y_next = next_point[1]

                # Simple crossing rule
                crossings = 0
                # Look at all points at this x
                for x_check in [x_val]:
                    # Check edges crossing this y
                    for j in range(n):
                        xj1, yj1 = points[j]
                        xj2, yj2 = points[(j + 1) % n]

                        # Check if edge crosses horizontal line at y
                        if ((yj1 <= y < yj2) or (yj2 <= y < yj1)) and xj1 == xj2:
                            # Vertical edge crossing
                            crossings += 1

                if crossings % 2 == 1:  # Inside
                    # Find next crossing
                    next_x = max_x + 1
                    for j in range(i + 1, len(intersections)):
                        if intersections[j][2] == 'cross':
                            next_x = intersections[j][0]
                            break

                    # Fill between current x and next x
                    for x in range(x_val, next_x + 1):
                        valid_tiles.add((x, y))

                    # Skip to next crossing
                    while i < len(intersections) and intersections[i][0] <= next_x:
                        i += 1
                else:
                    i += 1

    return valid_tiles


def is_rectangle_valid(x1, x2, y1, y2, valid_tiles):
    """Check if all points in rectangle are valid"""
    min_x, max_x = sorted([x1, x2])
    min_y, max_y = sorted([y1, y2])

    # Quick check: corners must be red
    if (x1, y1) not in valid_tiles or (x2, y2) not in valid_tiles:
        return False

    # Check all points in rectangle
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in valid_tiles:
                return False
    return True


def solve_part2_fast(filename):
    print("Reading input...")
    points = read_points(filename)
    print(f"Read {len(points)} red points")

    print("Identifying red and green tiles...")
    valid_tiles = get_all_valid_tiles(points)
    print(f"Found {len(valid_tiles)} valid (red/green) tiles")

    # Filter to only red points for corner checking
    red_set = set(points)
    red_list = list(red_set)

    print("Searching for largest valid rectangle...")
    max_area = 0
    best_corners = None
    n = len(red_list)

    # Progress tracking
    total_pairs = n * (n - 1) // 2
    processed = 0
    progress_step = max(1, total_pairs // 100)  # Update progress ~100 times

    for i in range(n):
        x1, y1 = red_list[i]
        for j in range(i + 1, n):
            x2, y2 = red_list[j]

            # Must have different x and y
            if x1 == x2 or y1 == y2:
                continue

            # Check rectangle
            if is_rectangle_valid(x1, x2, y1, y2, valid_tiles):
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height

                if area > max_area:
                    max_area = area
                    best_corners = ((x1, y1), (x2, y2))

            # Progress update
            processed += 1
            if processed % progress_step == 0:
                percent = (processed / total_pairs) * 100
                sys.stdout.write(f"\rProgress: {percent:.1f}% ({processed}/{total_pairs} pairs)")
                sys.stdout.flush()

    print(f"\nSearch complete!")

    if best_corners:
        print(f"\nBest rectangle found:")
        print(f"  Corner 1: {best_corners[0]}")
        print(f"  Corner 2: {best_corners[1]}")
        width = abs(best_corners[0][0] - best_corners[1][0]) + 1
        height = abs(best_corners[0][1] - best_corners[1][1]) + 1
        print(f"  Width: {width}, Height: {height}")

    return max_area


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'day9_input.txt'

    try:
        result = solve_part2_fast(input_file)

        print(f"\n{'=' * 50}")
        print(f"Largest rectangle area: {result}")
        print(f"{'=' * 50}")

        # Save to file
        with open('day9_output.txt', 'w') as f:
            f.write(str(result))

        print(f"\nResult saved to 'day9_output.txt'")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        print("Usage: python day9_solution.py [input_file.txt]")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()