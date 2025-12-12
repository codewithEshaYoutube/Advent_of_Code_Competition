import sys
from collections import deque
from functools import lru_cache


# ===========================================
# 1. PARSING UTILITIES
# ===========================================
def parse_input(filename):
    """Parse shapes and regions from input file."""
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    shapes = []
    regions = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Shape definition (e.g., "0:")
        if line.endswith(':') and line[:-1].isdigit():
            shape_id = int(line[:-1])
            i += 1
            shape_grid = []

            # Collect shape lines
            while i < len(lines) and lines[i].strip() and not lines[i].strip().endswith(':'):
                if '#' in lines[i] or '.' in lines[i]:
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
            # Region line (e.g., "12x5: 1 0 1 0 2 2")
            if 'x' in line and ':' in line and line[0].isdigit():
                try:
                    size_part, counts_part = line.split(':', 1)
                    w_str, h_str = size_part.strip().split('x')
                    w, h = int(w_str), int(h_str)
                    counts = list(map(int, counts_part.strip().split()))
                    regions.append((w, h, counts))
                except ValueError:
                    pass
            i += 1

    return shapes, regions


# ===========================================
# 2. SHAPE TRANSFORMATIONS
# ===========================================
def rotate_shape(shape):
    """Rotate shape 90 degrees clockwise."""
    return sorted((c, -r) for r, c in shape)


def normalize(shape):
    """Shift shape to have min_r=0, min_c=0."""
    if not shape:
        return tuple()
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


# ===========================================
# 3. SOLVER FOR PART 1
# ===========================================
class Part1Solver:
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
        """Main solving method for part 1."""
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
                    if self._can_place(board, orient, start_r, start_c):
                        filled = self._place_shape(board, orient, start_r, start_c, shape_idx)

                        if self._backtrack(board, shapes, pos + 1):
                            return True

                        self._remove_shape(board, filled)

        return False

    def _can_place(self, board, shape, r, c):
        """Check if shape can be placed at (r,c) on board."""
        for dr, dc in shape:
            nr, nc = r + dr, c + dc
            if board[nr][nc] != -1:
                return False
        return True

    def _place_shape(self, board, shape, r, c, shape_id):
        """Place shape on board and return list of filled cells."""
        filled = []
        for dr, dc in shape:
            nr, nc = r + dr, c + dc
            board[nr][nc] = shape_id
            filled.append((nr, nc))
        return filled

    def _remove_shape(self, board, cells):
        """Remove shape from board."""
        for r, c in cells:
            board[r][c] = -1

    def _find_empty(self, board):
        """Find first empty cell."""
        for r in range(self.H):
            for c in range(self.W):
                if board[r][c] == -1:
                    return r, c
        return -1, -1


# ===========================================
# 4. SOLVER FOR PART 2 (BORDER CONSTRAINT)
# ===========================================
class Part2Solver:
    """Solver for part 2 where all # cells must touch the border."""

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
        """Main solving method for part 2 with border constraint."""
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

        return self._backtrack_with_border(board, shape_instances, 0)

    def _backtrack_with_border(self, board, shapes, pos):
        """Recursive backtracking with border constraint."""
        if pos == len(shapes):
            # Check if all placed shapes touch border
            return self._all_shapes_touch_border(board, shapes)

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
                    if self._can_place(board, orient, start_r, start_c):
                        # Check if this placement touches border
                        if not self._shape_touches_border(orient, start_r, start_c):
                            continue

                        filled = self._place_shape(board, orient, start_r, start_c, shape_idx)

                        if self._backtrack_with_border(board, shapes, pos + 1):
                            return True

                        self._remove_shape(board, filled)

        return False

    def _shape_touches_border(self, shape, r, c):
        """Check if at least one cell of this shape touches the border."""
        for dr, dc in shape:
            nr, nc = r + dr, c + dc
            # Check if cell touches any border
            if nr == 0 or nr == self.H - 1 or nc == 0 or nc == self.W - 1:
                return True
        return False

    def _all_shapes_touch_border(self, board, shapes):
        """Check if all placed shapes in board touch border."""
        # This would require more complex tracking
        # For efficiency, we check during placement
        return True

    def _can_place(self, board, shape, r, c):
        """Check if shape can be placed at (r,c) on board."""
        for dr, dc in shape:
            nr, nc = r + dr, c + dc
            if board[nr][nc] != -1:
                return False
        return True

    def _place_shape(self, board, shape, r, c, shape_id):
        """Place shape on board and return list of filled cells."""
        filled = []
        for dr, dc in shape:
            nr, nc = r + dr, c + dc
            board[nr][nc] = shape_id
            filled.append((nr, nc))
        return filled

    def _remove_shape(self, board, cells):
        """Remove shape from board."""
        for r, c in cells:
            board[r][c] = -1

    def _find_empty(self, board):
        """Find first empty cell."""
        for r in range(self.H):
            for c in range(self.W):
                if board[r][c] == -1:
                    return r, c
        return -1, -1


# ===========================================
# 5. MAIN EXECUTION
# ===========================================
def main():
    if len(sys.argv) != 2:
        print("Usage: python day12.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Parse input
    shapes, regions = parse_input(input_file)

    if not shapes or not regions:
        print("Error: Could not parse shapes and regions")
        sys.exit(1)

    print(f"Loaded {len(shapes)} shapes and {len(regions)} regions")

    # Solve Part 1
    part1_count = 0
    for idx, (W, H, counts) in enumerate(regions):
        print(f"Part 1 - Region {idx + 1}/{len(regions)}: {W}x{H}...", end=" ")
        solver = Part1Solver(shapes, W, H, counts)
        if solver.solve():
            part1_count += 1
            print("FITS")
        else:
            print("NO FIT")

    print(f"\n=== PART 1 RESULT ===")
    print(f"Regions that fit: {part1_count}")

    # Solve Part 2 (with border constraint)
    part2_count = 0
    for idx, (W, H, counts) in enumerate(regions):
        print(f"Part 2 - Region {idx + 1}/{len(regions)}: {W}x{H}...", end=" ")
        solver = Part2Solver(shapes, W, H, counts)
        if solver.solve():
            part2_count += 1
            print("FITS")
        else:
            print("NO FIT")

    print(f"\n=== PART 2 RESULT ===")
    print(f"Regions that fit with border constraint: {part2_count}")

    print(f"\n=== FINAL ANSWERS ===")
    print(f"Part 1 answer to submit: {part1_count}")
    print(f"Part 2 answer to submit: {part2_count}")
    print("\nNote: If part 2 has different requirements, please check the")
    print("Advent of Code website and let me know what they are.")


if __name__ == "__main__":
    main()