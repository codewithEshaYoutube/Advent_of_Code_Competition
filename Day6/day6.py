def parse_worksheet_part2(data):
    rows = data.strip().split('\n')
    max_len = max(len(r) for r in rows)
    rows = [r.ljust(max_len) for r in rows]
    n_rows = len(rows)
    n_num_rows = n_rows - 1

    # First, find all column indices that are all spaces -> separators
    separator_cols = []
    for col in range(max_len):
        if all(rows[r][col] == ' ' for r in range(n_rows)):
            separator_cols.append(col)

    # Add boundaries
    separator_cols = [-1] + separator_cols + [max_len]

    problems = []
    for i in range(len(separator_cols) - 1):
        start = separator_cols[i] + 1
        end = separator_cols[i + 1]
        if end > start:  # Non-empty problem
            # Extract this problem's subgrid
            prob_rows = [rows[r][start:end] for r in range(n_rows)]
            problems.append(prob_rows)

    results = []
    for prob_rows in problems:
        width = len(prob_rows[0])
        height = n_num_rows

        # Find numbers: consecutive non-space vertical columns
        numbers = []
        c = 0
        while c < width:
            # Skip empty vertical columns (between numbers within problem)
            if all(prob_rows[r][c] == ' ' for r in range(height)):
                c += 1
                continue

            # Start of a number
            num_digits = []
            while c < width and not all(prob_rows[r][c] == ' ' for r in range(height)):
                # Get digit column
                col_digits = [prob_rows[r][c] for r in range(height)]
                # Remove trailing spaces (from bottom), but keep order top to bottom
                while col_digits and col_digits[-1] == ' ':
                    col_digits.pop()
                num_digits.append(''.join(col_digits).strip())
                c += 1

            # Now num_digits has digit strings for each column
            # But wait: each column should be a single digit actually
            # Actually, in example: number 431 comes from columns: '4', '3', '1' vertically
            # So join them -> '431'
            number_str = ''
            for digit_col in num_digits:
                # digit_col might be like '4  ' (with spaces below), we took first char
                # Actually we should take the non-space chars top to bottom
                # But simpler: each digit_col string has digits possibly with spaces between?
                # Let's reconstruct properly:
                pass
            # Let me rethink: each digit is in one column top to bottom
            # So for number 431: column1: '4', column2: '3', column3: '1' (vertical)
            # We need to read top row first for most significant digit.

            # Actually, the digits are stacked vertically in one column per digit.
            # So for number with k digits, we need k columns.
            # In each column, the digits from top to bottom form... wait, each column has ONE digit at some row?
            # Actually no: In example, number 623: probably columns: first column has '6' at top row, spaces below?
            # This is confusing.

            # Let me check the given example transformation more carefully.