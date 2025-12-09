import sys


def read_points(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                points.append((x, y))
    return points


def get_connected_segments(points):
    """Return all grid points between consecutive red points (including endpoints)"""
    segments = []
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]  # wraps around

        if x1 == x2:  # vertical line
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                segments.append((x1, y))
        else:  # y1 == y2, horizontal line
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                segments.append((x, y1))
    return set(segments)


def is_point_in_polygon(x, y, polygon):
    """Ray casting algorithm to check if point is inside polygon"""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def get_all_green_red_tiles(points):
    """Get all tiles that are red or green (on boundary or inside polygon)"""
    # Boundary tiles (red + connecting green lines)
    boundary = get_connected_segments(points)

    # Find bounding box
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Expand bounding box a bit to include all possible interior
    min_x -= 1
    max_x += 1
    min_y -= 1
    max_y += 1

    # Get all interior points using ray casting
    all_valid = set(boundary)  # Start with boundary

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in boundary:
                if is_point_in_polygon(x, y, points):
                    all_valid.add((x, y))

    return all_valid


def rectangle_fully_in_region(x1, x2, y1, y2, valid_tiles):
    """Check if all tiles in rectangle are in valid region"""
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in valid_tiles:
                return False
    return True


def solve_part2(filename):
    points = read_points(filename)

    # Get all red/green tiles
    valid_tiles = get_all_green_red_tiles(points)

    # Create a set of just red points for quick lookup
    red_points = set(points)

    max_area = 0
    n = len(points)

    # Check all pairs of red points as potential opposite corners
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Need different x and y to be opposite corners
            if x1 == x2 or y1 == y2:
                continue

            # Check if rectangle is fully within red/green region
            if rectangle_fully_in_region(x1, x2, y1, y2, valid_tiles):
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height
                if area > max_area:
                    max_area = area

    return max_area


def main():
    # Assuming input is in day9_input.txt
    result = solve_part2('day9_input.txt')

    # Save to output file
    with open('day9_output.txt', 'w') as f:
        f.write(str(result))

    print(f"Part 2 Result: {result}")
    print("Output saved to day9_output.txt")


if __name__ == "__main__":
    main()