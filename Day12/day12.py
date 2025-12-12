import sys
import time
from collections import deque


# ------------------------------------------------------------
# 1. Parsing utilities
# ------------------------------------------------------------
def parse_input(filename):
    """Parse shapes and regions from input file."""
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    shapes = []
    regions = []

    i = 0
    # Parse shapes first
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Check if this is a shape definition (e.g., "0:")
        if line.endswith(':') and line[:-1].isdigit():
            shape_id = int(line[:-1])
            i += 1
            shape_grid = []

            # Collect shape lines until empty line or next shape/region
            while i < len(lines) and lines[i].strip() and not lines[i].strip().endswith(':'):
                shape_grid.append(lines[i].rstrip())
                i += 1

            # Convert to coordinates
            coords = []
            for r, row in enumerate(shape_grid):
                for c, ch in enumerate(row):
                    if ch == '#':
                        coords.append((r, c))

            if coords:
                # Normalize shape
                min_r = min(r for r, _ in coords)
                min_c = min(c for _, c in coords)
                normalized = [(r - min_r, c - min_c) for r, c in coords]
                shapes.append(sorted(normalized))
            else:
                i += 1
        else:
            # Check if this is a region line (e.g., "12x5: 1 0 1 0 2 2")
            if 'x' in line and ':' in line:
                size_part, counts_part = line.split(':', 1)
                try:
                    w_str, h_str = size_part.strip().split('x')
                    w = int(w_str)
                    h = int(h_str)
                    counts = list(map(int, counts_part.strip().split()))
                    regions.append((w, h, counts))
                except ValueError:
                    pass
            i += 1

    return shapes, regions


# ------------------------------------------------------------
# 2. Shape transformations
# ------------------------------------------------------------
def rotate_shape(shape):
    """Rotate shape 90 degrees clockwise."""
    return sorted((c, -r) for r, c in shape)


def normalize(shape):
    """Shift shape to have min_r=0, min_c=0."""
    min_r = min(r for r, _ in shape)
    min_c = min(c for _, c in shape)
    return tuple(sorted((r - min_r, c - min_c) for r, c in shape))


def generate_orientations(shape):
    """Generate all unique rotations and reflections of a shape."""
    orientations = set()

    # Original and rotations
    current = shape
    for _ in range(4):
        orientations.add(normalize(current))
        current = rotate_shape(current)

    # Reflect and rotations
    reflected = sorted((r, -c) for r, c in shape)
    current = reflected
    for _ in range(4):
        orientations.add(normalize(current))
        current = rotate_shape(current)

    return [list(orient) for orient in orientations]


# ------------------------------------------------------------
# 3. Board representation and placement
# ------------------------------------------------------------
def can_place(board, shape, r, c, W, H):
    """Check if shape can be placed at (r,c) on board."""
    for dr, dc in shape:
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= H or nc < 0 or nc >= W or board[nr][nc] != -1:
            return False
    return True


def place_shape(board, shape, r, c, shape_id):
    """Place shape on board and return list of filled cells."""
    filled = []
    for dr, dc in shape:
        nr, nc = r + dr, c + dc
        board[nr][nc] = shape_id
        filled.append((nr, nc))
    return filled


def remove_shape(board, cells):
    """Remove shape from board."""
    for r, c in cells:
        board[r][c] = -1


# ------------------------------------------------------------
# 4. Optimized solver with heuristics
# ------------------------------------------------------------
class Solver:
    def __init__(self, shapes, W, H, counts):
        self.W = W
        self.H = H
        self.total_cells = W * H

        # Generate orientations for each shape
        self.shape_orientations = []
        self.shape_sizes = []
        for shape in shapes:
            orientations = generate_orientations(shape)
            self.shape_orientations.append(orientations)
            self.shape_sizes.append(len(shape))

        # Counts of each shape to place
        self.original_counts = counts[:]
        self.num_shapes = len(counts)

        # Precompute shape dimensions for faster placement
        self.shape_dims = []
        for orientations in self.shape_orientations:
            dims = []
            for orient in orientations:
                max_r = max(r for r, _ in orient)
                max_c = max(c for _, c in orient)
                dims.append((max_r + 1, max_c + 1))
            self.shape_dims.append(dims)

    def solve(self):
        """Main solving method."""
        # Quick area check
        total_required = sum(cnt * size for cnt, size in zip(self.original_counts, self.shape_sizes))
        if total_required > self.total_cells:
            return False

        # Initialize board
        board = [[-1] * self.W for _ in range(self.H)]

        # Convert to list of shape instances with counts
        shape_instances = []
        for i, cnt in enumerate(self.original_counts):
            shape_instances.extend([i] * cnt)

        # Sort shapes by size (largest first)
        shape_instances.sort(key=lambda i: self.shape_sizes[i], reverse=True)

        return self._backtrack(board, shape_instances, 0)

    def _backtrack(self, board, shapes, pos):
        """Recursive backtracking."""
        if pos == len(shapes):
            return True

        shape_idx = shapes[pos]

        # Find first empty cell
        empty_r, empty_c = self._find_empty(board)
        if empty_r == -1:
            return False

        # Try all orientations of this shape
        for orient_idx, orient in enumerate(self.shape_orientations[shape_idx]):
            h, w = self.shape_dims[shape_idx][orient_idx]

            # Try all positions that cover the empty cell
            for dr, dc in orient:
                start_r = empty_r - dr
                start_c = empty_c - dc

                if 0 <= start_r and start_r + h <= self.H and 0 <= start_c and start_c + w <= self.W:
                    if can_place(board, orient, start_r, start_c, self.W, self.H):
                        filled = place_shape(board, orient, start_r, start_c, shape_idx)

                        # Check for small isolated empty areas
                        if self._has_small_hole(board):
                            remove_shape(board, filled)
                            continue

                        if self._backtrack(board, shapes, pos + 1):
                            return True

                        remove_shape(board, filled)

        return False

    def _find_empty(self, board):
        """Find first empty cell."""
        for r in range(self.H):
            for c in range(self.W):
                if board[r][c] == -1:
                    return r, c
        return -1, -1

    def _has_small_hole(self, board):
        """Check if there's an isolated empty area too small for any shape."""
        visited = [[False] * self.W for _ in range(self.H)]

        for r in range(self.H):
            for c in range(self.W):
                if board[r][c] == -1 and not visited[r][c]:
                    # BFS to find connected empty area
                    area = self._bfs_area(board, visited, r, c)
                    if area > 0:
                        # Check if this area could fit any remaining shape
                        min_shape_size = min(self.shape_sizes)
                        if area < min_shape_size:
                            return True
        return False

    def _bfs_area(self, board, visited, start_r, start_c):
        """BFS to find size of connected empty area."""
        area = 0
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True

        while queue:
            r, c = queue.popleft()
            area += 1

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.H and 0 <= nc < self.W:
                    if board[nr][nc] == -1 and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return area


# ------------------------------------------------------------
# 5. Main execution
# ------------------------------------------------------------
def main():
    start_time = time.time()

    # Parse input
    shapes, regions = parse_input('day12_input.txt')

    if not shapes:
        print("Error: No shapes found in input")
        return
    if not regions:
        print("Error: No regions found in input")
        return

    print(f"Loaded {len(shapes)} shapes and {len(regions)} regions")

    # Solve each region
    successful = 0
    results = []

    for idx, (W, H, counts) in enumerate(regions):
        print(f"Processing region {idx + 1}/{len(regions)}: {W}x{H}...", end=" ")

        # Filter shapes that have non-zero counts
        active_counts = counts
        solver = Solver(shapes, W, H, active_counts)

        if solver.solve():
            successful += 1
            results.append(f"{W}x{H}: {' '.join(map(str, counts))} -> fits")
            print("FITS")
        else:
            results.append(f"{W}x{H}: {' '.join(map(str, counts))} -> no fit")
            print("NO FIT")

    # Write output
    with open('day12_output.txt', 'w') as f:
        f.write(f"Total regions that fit: {successful}\n")
        f.write(f"Total time: {time.time() - start_time:.2f} seconds\n")
        f.write("=" * 50 + "\n")
        for result in results:
            f.write(result + "\n")

    print(f"\n{'=' * 50}")
    print(f"Total regions that fit: {successful}")
    print(f"Total time: {time.time() - start_time:.2f} seconds")
    print(f"Results written to day12_output.txt")


if __name__ == "__main__":
    main()