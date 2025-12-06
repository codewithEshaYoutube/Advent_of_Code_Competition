def parse_part2(data):
    """
    Parse worksheet for Part Two where numbers are written vertically
    and read right-to-left in columns.
    """
    rows = data.rstrip('\n').split('\n')
    max_len = max(len(r) for r in rows)

    # Pad all rows to same length
    rows = [r.ljust(max_len) for r in rows]
    n_rows = len(rows)
    n_num_rows = n_rows - 1  # Last row is operators

    grand_total = 0
    col = max_len - 1  # Start from rightmost column

    while col >= 0:
        # Skip separator columns (all spaces in all rows)
        if all(rows[r][col] == ' ' for r in range(n_rows)):
            col -= 1
            continue

        # Found a non-blank column - this is the end of a problem
        problem_end = col

        # Find the start of this problem (go left until we find operator or separator)
        problem_start = col
        while problem_start >= 0:
            # Check if this is a separator column
            if all(rows[r][problem_start] == ' ' for r in range(n_rows)):
                break

            # Check if this column has an operator in the bottom row
            if rows[n_num_rows][problem_start] in '+*':
                break

            problem_start -= 1

        # Adjust problem_start to the actual start (operator column)
        if problem_start < 0 or all(rows[r][problem_start] == ' ' for r in range(n_rows)):
            # No operator found, skip
            col -= 1
            continue

        # Now we have a problem from problem_start to problem_end
        op_char = rows[n_num_rows][problem_start]

        # Extract numbers from each column in the problem
        numbers = []
        for c in range(problem_start, problem_end + 1):
            # Get digits from top to bottom in this column
            digits = []
            for r in range(n_num_rows):
                char = rows[r][c]
                if char != ' ':
                    digits.append(char)

            if digits:
                number_str = ''.join(digits)
                numbers.append(int(number_str))

        # Apply the operation
        if op_char == '*':
            result = 1
            for n in numbers:
                result *= n
        else:  # '+'
            result = sum(numbers)

        grand_total += result

        # Move to next problem (left of current problem)
        col = problem_start - 1

    return grand_total


def main():
    try:
        with open('day6_input.txt', 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: day6_input.txt not found!")
        print("Please save your puzzle input to day6_input.txt")
        return

    result = parse_part2(data)

    # Output to console
    print(f"Part Two Grand Total: {result}")

    # Also save to file
    with open('day6_part2_output.txt', 'w') as f:
        f.write(str(result))
    print(f"Result also saved to day6_part2_output.txt")


if __name__ == "__main__":
    main()