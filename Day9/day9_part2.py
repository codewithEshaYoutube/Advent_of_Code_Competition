import sys


def read_points(filename):
    """Read red tile coordinates from file"""
    with open(filename) as f:
        return [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]


def is_point_inside(x, y, polygon):
    """Check if point is inside polygon using ray casting"""
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        # Check if edge crosses horizontal line at y
        if (y1 > y) != (y2 > y):
            # Calculate x intersection
            x_intersect = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x_intersect > x:
                inside = not inside

    return inside


def get_red_green_tiles(polygon):
    """Get all red and green tiles (boundary + interior)"""
    # Start with empty set
    tiles = set()
    n = len(polygon)

    # Step 1: Add all boundary tiles
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        if x1 == x2:  # Vertical line
            start_y, end_y = sorted([y1, y2])
            for y in range(start_y, end_y + 1):
                tiles.add((x1, y))
        else:  # Horizontal line
            start_x, end_x = sorted([x1, x2])
            for x in range(start_x, end_x + 1):
                tiles.add((x, y1))

    # Step 2: Find bounding box
    xs = [x for x, _ in polygon]
    ys = [y for _, y in polygon]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Step 3: Add interior points
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in tiles:
                if is_point_inside(x, y, polygon):
                    tiles.add((x, y))

    return tiles


def find_largest_rectangle(points):
    """Find largest rectangle with red corners inside red/green region"""
    # Get all red and green tiles
    red_green_tiles = get_red_green_tiles(points)
    red_set = set(points)

    max_area = 0
    n = len(points)

    # Check all pairs of red points
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Must be opposite corners
            if x1 == x2 or y1 == y2:
                continue

            # Get rectangle bounds
            min_x, max_x = sorted([x1, x2])
            min_y, max_y = sorted([y1, y2])

            # Check if all tiles in rectangle are red/green
            valid = True
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (x, y) not in red_green_tiles:
                        valid = False
                        break
                if not valid:
                    break

            if valid:
                width = max_x - min_x + 1
                height = max_y - min_y + 1
                area = width * height
                if area > max_area:
                    max_area = area

    return max_area


def main():
    print("🎬 Day 9: Movie Theater (Part 2)")
    print("=" * 40)

    # Read input
    try:
        points = read_points('day9_input.txt')
        print(f"📊 Read {len(points)} red tiles")
    except FileNotFoundError:
        print("❌ ERROR: day9_input.txt not found!")
        print("   Make sure the file is in the current directory.")
        return

    # Calculate answer
    print("⏳ Calculating...")
    answer = find_largest_rectangle(points)

    # Display result
    print("\n" + "=" * 40)
    print(f"✅ Answer: {answer}")
    print("=" * 40)

    # Save to file
    with open('day9_output.txt', 'w') as f:
        f.write(str(answer))
    print(f"💾 Saved to day9_output.txt")


if __name__ == "__main__":
    main()