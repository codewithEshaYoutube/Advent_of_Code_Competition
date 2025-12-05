def solve():
    # Read the input file
    with open('day5_input.txt', 'r') as f:
        lines = f.readlines()

    ranges = []

    # Parse until we hit a blank line (or end of file)
    for line in lines:
        line = line.strip()
        if not line:  # Empty line = end of ranges section
            break
        if '-' in line:
            a, b = map(int, line.split('-'))
            ranges.append((a, b))

    # Find all unique IDs in ranges
    all_ids = set()
    for start, end in ranges:
        for i in range(start, end + 1):
            all_ids.add(i)

    result = len(all_ids)

    # Print result
    print(f"Answer: {result}")

    # Save to output file
    with open('day5_output.txt', 'w') as f:
        f.write(str(result))

    return result


# Run the solution
if __name__ == "__main__":
    solve()