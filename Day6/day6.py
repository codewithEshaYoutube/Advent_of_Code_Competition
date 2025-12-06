def parse_worksheet(data):
    """
    Parse the worksheet data and return the grand total of all problems.
    """
    rows = data.strip().split('\n')
    max_len = max(len(r) for r in rows)

    # Pad all rows to the same length
    rows = [r.ljust(max_len) for r in rows]
    n_rows = len(rows)
    n_num_rows = n_rows - 1  # Last row is operators

    problems = []  # Will store lists of column characters for each problem
    current_problem_cols = []

    # Scan column by column
    for col in range(max_len):
        column_chars = [rows[r][col] for r in range(n_rows)]

        # Check if this is a separator column (all spaces)
        if all(ch == ' ' for ch in column_chars):
            if current_problem_cols:
                problems.append(current_problem_cols)
                current_problem_cols = []
        else:
            current_problem_cols.append(column_chars)

    # Don't forget the last problem if there is one
    if current_problem_cols:
        problems.append(current_problem_cols)

    # Calculate results for each problem
    results = []
    for prob_cols in problems:
        # Extract numbers from each number row
        num_vals = []
        for r in range(n_num_rows):
            # Join all characters in this row across the problem's columns
            num_str = ''.join(prob_cols[c][r] for c in range(len(prob_cols)))
            num_str = num_str.strip()
            if num_str:
                num_vals.append(int(num_str))

        # Extract operator from the last row
        op_row = ''.join(prob_cols[c][n_num_rows] for c in range(len(prob_cols)))
        op_char = op_row.strip()[0]  # Get the first non-space character

        # Calculate based on operator
        if op_char == '*':
            result = 1
            for n in num_vals:
                result *= n
        else:  # '+'
            result = sum(num_vals)

        results.append(result)

    grand_total = sum(results)
    return grand_total, results


def main():
    # Read input from file
    try:
        with open('day6_input.txt', 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: day6_input.txt not found!")
        return

    # Parse worksheet and get results
    grand_total, individual_results = parse_worksheet(data)

    # Display results
    print(f"Number of problems solved: {len(individual_results)}")
    print(f"Grand total: {grand_total}")

    # Save output to file
    with open('day6_output.txt', 'w') as f:
        f.write(f"Grand total: {grand_total}\n")
        f.write(f"Number of problems: {len(individual_results)}\n")
        f.write("\nIndividual problem results:\n")
        for i, result in enumerate(individual_results, 1):
            f.write(f"Problem {i}: {result}\n")

    print("Results saved to day6_output.txt")


if __name__ == "__main__":
    main()