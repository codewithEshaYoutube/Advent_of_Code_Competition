def count_splits(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position
    start_col = None
    for j in range(cols):
        if grid[0][j] == 'S':
            start_col = j
            break

    if start_col is None:
        return 0

    # We'll process row by row since beams always go down
    # Track active beams at each column
    active_beams = {start_col}
    splits = 0

    for i in range(1, rows):  # Start from row below S
        new_active_beams = set()

        # Process each active beam from previous row
        for col in active_beams:
            # Beam moves down to current row
            cell = grid[i][col]

            if cell == '^':
                # Split occurs!
                splits += 1
                # New beams start from left and right of splitter
                if col > 0:
                    new_active_beams.add(col - 1)
                if col < cols - 1:
                    new_active_beams.add(col + 1)
            else:
                # Beam continues downward
                new_active_beams.add(col)

        active_beams = new_active_beams

    return splits


# Read input from file
with open('day7_input.txt', 'r') as f:
    grid = [line.rstrip('\n') for line in f]

result = count_splits(grid)

# Save answer to output file
with open('day7_output.txt', 'w') as f:
    f.write(str(result))

print(f"Number of splits: {result}")
print("Answer saved to day7_output.txt")