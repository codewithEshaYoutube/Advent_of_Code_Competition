def solve():
    with open('day5_input.txt', 'r') as f:
        content = f.read()

    # Split by the blank line
    parts = content.strip().split('\n\n')

    if len(parts) < 1:
        print("Invalid input format")
        return 0

    # Parse only the ranges from the first part (before blank line)
    ranges = []
    for line in parts[0].strip().split('\n'):
        line = line.strip()
        if line and '-' in line:
            a, b = map(int, line.split('-'))
            ranges.append((a, b))

    print(f"Number of ranges: {len(ranges)}")

    # Find all unique IDs covered by any range
    # Since the numbers are large, we need an efficient approach
    # Sort ranges by start
    ranges.sort(key=lambda x: x[0])

    # Merge overlapping ranges
    merged_ranges = []
    current_start, current_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= current_end + 1:  # Overlapping or adjacent
            if end > current_end:
                current_end = end
        else:
            merged_ranges.append((current_start, current_end))
            current_start, current_end = start, end

    merged_ranges.append((current_start, current_end))

    print(f"Number of merged ranges: {len(merged_ranges)}")

    # Calculate total number of IDs
    total_ids = 0
    for start, end in merged_ranges:
        total_ids += (end - start + 1)

    print(f"Total unique IDs covered: {total_ids}")

    # Save to output file
    with open('day5_output.txt', 'w') as f:
        f.write(str(total_ids))

    return total_ids


if __name__ == "__main__":
    solve()