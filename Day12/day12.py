def solve_simple() -> int:
    with open('day12_input.txt', 'r') as f:
        data = f.read().strip()

    # Split into shapes block and regions block
    shapes_block, regions_block = data.split('\n\n')[-2:]

    # Parse regions: each line is like "12x5: 1 0 1 0 2 2"
    regions = []
    for line in regions_block.strip().split('\n'):
        if not line:
            continue
        size_part, counts_part = line.split(': ')
        width, height = map(int, size_part.split('x'))
        counts = list(map(int, counts_part.split()))
        regions.append((width, height, counts))

    # Count regions where total required cells <= grid cells
    fit_count = 0
    for width, height, counts in regions:
        total_required_cells = sum(count * 9 for count in counts)  # Each shape uses 9 cells (#)
        if total_required_cells <= width * height:
            fit_count += 1

    return fit_count

print(solve_simple())