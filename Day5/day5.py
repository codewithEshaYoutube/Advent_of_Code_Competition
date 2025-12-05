def solve():
    with open('day5_input.txt', 'r') as f:
        content = f.read().strip()

    # Split into two parts by blank line
    parts = content.split('\n\n')

    if len(parts) != 2:
        print("Invalid input format")
        return

    # Parse ranges
    ranges = []
    for line in parts[0].strip().split('\n'):
        a, b = map(int, line.split('-'))
        ranges.append((a, b))

    # Parse available IDs
    available_ids = list(map(int, parts[1].strip().split('\n')))

    # Count fresh IDs
    fresh_count = 0

    for ingredient_id in available_ids:
        # Check if ID is in any range
        is_fresh = False
        for a, b in ranges:
            if a <= ingredient_id <= b:
                is_fresh = True
                break

        if is_fresh:
            fresh_count += 1

    print(f"Number of fresh ingredient IDs: {fresh_count}")

    # Save output to file
    with open('day5_output.txt', 'w') as f:
        f.write(str(fresh_count))

    return fresh_count


if __name__ == "__main__":
    result = solve()