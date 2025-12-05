def count_adjacent_ats(grid, r, c, rows, cols):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '@':
                    count += 1
    return count

def solve():
    with open("day4_input.txt", "r") as f:
        grid = [list(line.strip()) for line in f]

    rows = len(grid)
    cols = len(grid[0])

    total_removed = 0

    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    if count_adjacent_ats(grid, r, c, rows, cols) < 4:
                        to_remove.append((r, c))

        if not to_remove:
            break

        # Remove them
        for r, c in to_remove:
            grid[r][c] = '.'

        total_removed += len(to_remove)

    print(total_removed)

if __name__ == "__main__":
    solve()