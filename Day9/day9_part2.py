import sys


def read_points(filename):
    with open(filename) as f:
        return [tuple(map(int, line.split(','))) for line in f if line.strip()]


def get_valid_tiles(points):
    """Get all red and green tiles using ray casting"""
    # All red points
    valid = set(points)

    # Connect points to form closed polygon (add boundary green tiles)
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        if x1 == x2:  # vertical
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                valid.add((x1, y))
        else:  # horizontal
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                valid.add((x, y1))

    # Find bounding box
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Use ray casting to fill interior
    # For each point in bounding box, check if inside polygon
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in valid:
                continue  # Already marked as red or boundary green

            # Ray casting algorithm
            inside = False
            for i in range(n):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % n]

                # Check if point is on edge
                if min(y1, y2) <= y <= max(y1, y2):
                    if y1 == y2 and x1 <= x <= x2:
                        # On horizontal edge
                        inside = True
                        break
                    elif y1 != y2:
                        # Calculate x intersection
                        if x1 == x2:  # Vertical edge
                            if x == x1:
                                inside = True
                                break
                        else:
                            # Not vertical, calculate intersection
                            x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                            if abs(x - x_intersect) < 1e-9:
                                inside = True
                                break

            if inside:
                # Check if actually inside using winding number
                winding = 0
                for i in range(n):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % n]

                    if y1 <= y:
                        if y2 > y and (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) > 0:
                            winding += 1
                    else:
                        if y2 <= y and (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) < 0:
                            winding -= 1

                if winding != 0:
                    valid.add((x, y))

    return valid


def solve():
    points = read_points('day9_input.txt')
    valid_tiles = get_valid_tiles(points)

    # Create a list of unique red points
    red_points = list(set(points))
    n = len(red_points)

    max_area = 0

    for i in range(n):
        x1, y1 = red_points[i]
        for j in range(i + 1, n):
            x2, y2 = red_points[j]

            if x1 == x2 or y1 == y2:
                continue

            # Get rectangle bounds
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            # Quick check: both corners must be red
            if (x1, y1) not in points or (x2, y2) not in points:
                continue

            # Check all tiles in rectangle
            valid_rect = True
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (x, y) not in valid_tiles:
                        valid_rect = False
                        break
                if not valid_rect:
                    break

            if valid_rect:
                area = (max_x - min_x + 1) * (max_y - min_y + 1)
                if area > max_area:
                    max_area = area

    return max_area


if __name__ == '__main__':
    result = solve()
    print(f"Solution: {result}")
    with open('day9_output.txt', 'w') as f:
        f.write(str(result))