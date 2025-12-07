def count_timelines(grid):
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

    # Track possible positions at current row (quantum superposition)
    # Using a set since order doesn't matter
    possible_positions = {start_col}

    for i in range(1, rows):  # Start from row below S
        new_positions = set()

        # For each possible position in previous row
        for col in possible_positions:
            cell = grid[i][col]

            if cell == '^':
                # Quantum split: particle goes to BOTH left and right
                if col > 0:
                    new_positions.add(col - 1)
                if col < cols - 1:
                    new_positions.add(col + 1)
            else:
                # Particle continues straight down
                new_positions.add(col)

        possible_positions = new_positions

    # Number of timelines = number of distinct end positions
    return len(possible_positions)


# Read input from file
with open('day7_input.txt', 'r') as f:
    grid = [line.rstrip('\n') for line in f]

result = count_timelines(grid)

# Save answer to output file
with open('day7_output2.txt', 'w') as f:
    f.write(str(result))

print(f"Number of timelines: {result}")
print("Answer saved to day7_output2.txt")