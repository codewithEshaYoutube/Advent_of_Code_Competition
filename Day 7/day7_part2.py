def count_timelines(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position
    start_col = None
    for j in range(cols):
        if grid[0][j] == 'S':
            start_col = j
            break

    # Memoization: (row, col) -> number of paths from here to bottom
    memo = {}

    def dfs(row, col):
        # Check memo
        if (row, col) in memo:
            return memo[(row, col)]

        # If at bottom row, we have one complete path
        if row == rows - 1:
            return 1

        # Check current cell
        cell = grid[row][col]

        total_paths = 0

        if cell == '^':
            # At splitter: can go left OR right to adjacent cells in SAME row
            # Then continue downward from there
            if col > 0:
                # Go left
                total_paths += dfs(row, col - 1)
            if col < cols - 1:
                # Go right
                total_paths += dfs(row, col + 1)
        else:
            # Not at splitter: continue straight down
            total_paths += dfs(row + 1, col)

        memo[(row, col)] = total_paths
        return total_paths

    result = dfs(0, start_col)
    return result


# Read input from file
with open('day7_input.txt', 'r') as f:
    grid = [line.rstrip('\n') for line in f]

result = count_timelines(grid)

# Save answer to output file
with open('day7_output2.txt', 'w') as f:
    f.write(str(result))

print(f"Number of timelines: {result}")
print("Answer saved to day7_output2.txt")