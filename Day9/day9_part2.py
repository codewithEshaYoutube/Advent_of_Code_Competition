import sys
from collections import defaultdict


def read_input(filename='day9_input.txt'):
    """Read red tile coordinates from file"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    reds = []
    for line in lines:
        line = line.strip()
        if line:
            x_str, y_str = line.split(',')
            reds.append((int(x_str), int(y_str)))
    return reds


def collect_horizontal(edges):
    """Collect horizontal edges grouped by y coordinate"""
    horizontal = defaultdict(list)
    for ((x1, y1), (x2, y2)) in edges:
        if y1 == y2:
            horizontal[y1].append((min(x1, x2), max(x1, x2)))
    return horizontal


def build_vertical_edge_map(edges, min_y, max_y):
    """Build map of vertical edges for each y coordinate"""
    vertical = defaultdict(list)
    for ((x1, y1), (x2, y2)) in edges:
        if x1 != x2:
            continue
        # This is a vertical edge
        ylo = min(y1, y2)
        yhi = max(y1, y2)
        # Add to Y values in range [ylo, yhi)
        for y in range(max(min_y, ylo), min(max_y, yhi - 1) + 1):
            vertical[y].append(x1)

    # Sort the x values for each y
    for y in vertical:
        vertical[y].sort()

    return vertical


def merge_segments(segments):
    """Merge overlapping or adjacent segments"""
    if not segments:
        return []

    segments.sort(key=lambda x: x[0])
    result = [segments[0]]

    for a, b in segments[1:]:
        c, d = result[-1]
        if a <= d + 1:
            # Overlapping or adjacent
            result[-1] = (c, max(d, b))
        else:
            result.append((a, b))

    return result


def pair_up(lst):
    """Convert list [a, b, c, d] to pairs [(a, b), (c, d)]"""
    result = []
    i = 0
    while i + 1 < len(lst):
        result.append((lst[i], lst[i + 1]))
        i += 2
    return result


def solve():
    """Main solving function"""
    print("Solving Day 9 Part 2...")
    print("=" * 40)

    try:
        # Read input from day9_input.txt
        reds = read_input('day9_input.txt')
        print(f"✓ Read {len(reds)} red tiles")
    except FileNotFoundError:
        print("✗ ERROR: day9_input.txt not found!")
        print("  Make sure the file is in the current directory")
        return 0

    if not reds:
        return 0

    # Create edges between consecutive points (with wrap-around)
    edges = list(zip(reds, reds[1:] + [reds[0]]))

    # Collect horizontal edges
    horizontal_list = collect_horizontal(edges)
    horizontal_map = {}
    for y, segs in horizontal_list.items():
        horizontal_map[y] = merge_segments(segs)

    # Get y range
    all_y = [y for _, y in reds]
    min_y, max_y = min(all_y), max(all_y)
    print(f"✓ Y-range: {min_y} to {max_y}")

    # Build vertical edge map
    vertical_map = build_vertical_edge_map(edges, min_y, max_y)
    print(f"✓ Processed {len(edges)} edges")

    # Build map of valid x-ranges for each y
    print("✓ Building valid x-ranges map...")
    valid_x_ranges_map = {}
    for y in range(min_y, max_y + 1):
        horz_segs = horizontal_map.get(y, [])
        crossings = vertical_map.get(y, [])
        interior_ranges = pair_up(crossings)
        all_ranges = horz_segs + interior_ranges
        valid_x_ranges_map[y] = merge_segments(all_ranges)

    def valid_rectangle(p1, p2):
        """Check if rectangle defined by opposite corners p1 and p2 is valid"""
        x1, y1 = p1
        x2, y2 = p2
        xlo = min(x1, x2)
        xhi = max(x1, x2)
        ylo = min(y1, y2)
        yhi = max(y1, y2)

        def valid_for_y(y):
            ranges = valid_x_ranges_map.get(y, [])
            return any(a <= xlo and xhi <= b for a, b in ranges)

        # Check all corners and all rows
        if not (valid_for_y(ylo) and valid_for_y(yhi)):
            return False

        # Check all rows in between
        for y in range(ylo, yhi + 1):
            if not valid_for_y(y):
                return False

        return True

    # Generate candidate rectangles
    print("✓ Checking all rectangle pairs...")
    max_area = 0
    n = len(reds)
    total_pairs = n * (n - 1) // 2
    checked = 0

    for i in range(n):
        x1, y1 = reds[i]
        for j in range(i + 1, n):
            x2, y2 = reds[j]
            checked += 1

            # Show progress
            if checked % 10000 == 0:
                percent = (checked / total_pairs) * 100
                print(f"  Progress: {percent:.1f}% ({checked}/{total_pairs})", end='\r')

            if x1 == x2 or y1 == y2:
                continue  # Not opposite corners

            if valid_rectangle((x1, y1), (x2, y2)):
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height
                if area > max_area:
                    max_area = area

    print(" " * 50, end='\r')  # Clear progress line

    return max_area


def main():
    # Run the solver
    result = solve()

    print("\n" + "=" * 40)
    print(f"✅ Largest rectangle area: {result}")
    print("=" * 40)

    # Save to output file
    with open('day9_output.txt', 'w') as f:
        f.write(str(result))
    print(f"💾 Result saved to 'day9_output.txt'")

    return result


if __name__ == "__main__":
    main()