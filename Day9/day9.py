import sys


def largest_rectangle_area(points):
    # Store points in a set for O(1) lookup
    point_set = set(points)
    max_area = 0

    # Try all pairs of points
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Opposite corners must have different x and y
            if x1 == x2 or y1 == y2:
                continue

            # Both (x1,y1) and (x2,y2) are in point_set (they are red tiles)
            # The rectangle's other corners are (x1,y2) and (x2,y1)
            # No requirement that those other corners are red

            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            if area > max_area:
                max_area = area

    return max_area


def main():
    # Read input from file
    try:
        with open('day9_input.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: day9_input.txt not found")
        sys.exit(1)

    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(','))
        points.append((x, y))

    # Calculate result
    result = largest_rectangle_area(points)

    # Save output to file
    with open('day9_output.txt', 'w') as f:
        f.write(str(result))

    print(f"Result: {result}")
    print("Output saved to day9_output.txt")


if __name__ == "__main__":
    main()