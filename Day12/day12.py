import sys
from collections import defaultdict
from itertools import product
import time


# ------------------------------------------------------------
# 1. Bitmask representation utilities
# ------------------------------------------------------------
def coords_to_mask(coords, width):
    """Convert list of (r,c) to integer bitmask for width x height grid."""
    mask = 0
    for r, c in coords:
        mask |= 1 << (r * width + c)
    return mask


def mask_to_coords(mask, width):
    """Convert mask back to coords (for debugging)."""
    coords = []
    bit = 0
    while mask:
        if mask & 1:
            r, c = divmod(bit, width)
            coords.append((r, c))
        mask >>= 1
        bit += 1
    return coords


def can_place_mask(grid_mask, shape_mask, pos_mask):
    """Check if shape_mask shifted by pos_mask fits in grid_mask without overlap."""
    return (grid_mask & shape_mask) == 0


def get_shape_dimensions(coords):
    """Get height and width of shape from coords."""
    rows = [r for r, _ in coords]
    cols = [c for _, c in coords]
    return max(rows) - min(rows) + 1, max(cols) - min(cols) + 1


# ------------------------------------------------------------
# 2. Shape parsing and orientation generation
# ------------------------------------------------------------
def normalize_shape(coords):
    """Shift shape to have min_r=0, min_c=0."""
    min_r = min(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    return tuple(sorted((r - min_r, c - min_c) for r, c in coords))


def rotate90_coords(coords):
    """Rotate coordinates 90 degrees clockwise: (r, c) -> (c, -r)."""
    rotated = [(c, -r) for r, c in coords]
    return normalize_shape(rotated)


def reflect_coords(coords):
    """Reflect over vertical axis: (r, c) -> (r, -c)."""
    reflected = [(r, -c) for r, c in coords]
    return normalize_shape(reflected)


def generate_unique_orientations(coords):
    """Generate all unique rotations/flips of a shape."""
    orientations = set()
    current = coords

    # 4 rotations
    for _ in range(4):
        orientations.add(current)
        current = rotate90_coords(current)

    # Reflect and 4 rotations
    reflected = reflect_coords(coords)
    current = reflected
    for _ in range(4):
        orientations.add(current)
        current = rotate90_coords(current)

    return [list(orient) for orient in orientations]


def precompute_shape_placements(shape_coords_list, grid_w, grid_h):
    """
    For each shape orientation, precompute all valid placements as (mask, area_mask).
    Returns: list_for_each_shape[orientation_index] = list_of_valid_placements
    """
    all_placements = []

    for shape_idx, orientations in enumerate(shape_coords_list):
        shape_placements = []
        for orient in orientations:
            placements = []
            h, w = get_shape_dimensions(orient)

            # For each possible top-left position
            for start_r in range(grid_h - h + 1):
                for start_c in range(grid_w - w + 1):
                    # Create mask for this position
                    mask = 0
                    for dr, dc in orient:
                        bit_pos = (start_r + dr) * grid_w + (start_c + dc)
                        mask |= 1 << bit_pos
                    placements.append(mask)

            shape_placements.append(placements)
        all_placements.append(shape_placements)

    return all_placements


# ------------------------------------------------------------
# 3. Parsing
# ------------------------------------------------------------
def parse_input(lines):
    """Parse shapes and regions from input."""
    shapes = []
    regions = []

    i = 0
    # Parse shapes
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.endswith(':'):
            # New shape
            shape_idx = int(line[:-1])
            shape_grid = []
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().endswith(':'):
                if '#' in lines[i] or '.' in lines[i]:
                    shape_grid.append(lines[i].rstrip())
                i += 1
            else:
                i += 1

            # Extract coordinates
            coords = []
            for r, row in enumerate(shape_grid):
                for c, ch in enumerate(row):
                    if ch == '#':
                        coords.append((r, c))

            if coords:
                shapes.append(coords)
        else:
            # Check if region line
            if 'x' in line and ':' in line and line[0].isdigit():
                size_part, counts_part = line.split(':')
                w, h = map(int, size_part.split('x'))
                counts = list(map(int, counts_part.strip().split()))
                regions.append((w, h, counts))
            i += 1

    return shapes, regions


# ------------------------------------------------------------
# 4. Zobrist hashing for memoization
# ------------------------------------------------------------
class ZobristHash:
    def __init__(self, grid_size, num_shapes):
        self.grid_size = grid_size
        self.num_shapes = num_shapes
        self.hash_table = {}
        self._init_random_values()

    def _init_random_values(self):
        """Initialize random values for each (position, shape) pair."""
        import random
        random.seed(42)  # Deterministic

        self.cell_shape = []
        for _ in range(self.grid_size):
            row = []
            for _ in range(self.num_shapes + 1):  # +1 for empty
                row.append(random.getrandbits(64))
            self.cell_shape.append(row)

        self.shape_count = []
        for _ in range(self.num_shapes):
            count_vals = []
            max_count = 10  # Reasonable upper bound
            for _ in range(max_count + 1):
                count_vals.append(random.getrandbits(64))
            self.shape_count.append(count_vals)

    def hash_state(self, grid_mask, counts):
        """Compute hash for current state."""
        h = 0

        # Hash grid occupancy
        temp_mask = grid_mask
        pos = 0
        while temp_mask:
            if temp_mask & 1:
                shape_at_pos = 0  # For simplicity, we hash occupied as 1 shape type
                h ^= self.cell_shape[pos][shape_at_pos]
            temp_mask >>= 1
            pos += 1

        # Hash shape counts
        for shape_idx, count in enumerate(counts):
            h ^= self.shape_count[shape_idx][count]

        return h


# ------------------------------------------------------------
# 5. Optimized backtracking solver
# ------------------------------------------------------------
class PackingSolver:
    def __init__(self, shapes, grid_w, grid_h, counts):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.grid_size = grid_w * grid_h
        self.counts = counts[:]
        self.num_shapes = len(counts)

        # Generate orientations for each shape
        self.shape_orientations = []
        self.shape_sizes = []
        for coords in shapes:
            orientations = generate_unique_orientations(coords)
            self.shape_orientations.append(orientations)
            self.shape_sizes.append(len(orientations[0]))  # Number of cells

        # Precompute all valid placements as bitmasks
        self.placements = precompute_shape_placements(self.shape_orientations, grid_w, grid_h)

        # Sort shapes by size (largest first) for better pruning
        self.shape_order = sorted(range(self.num_shapes),
                                  key=lambda i: self.shape_sizes[i], reverse=True)

        # Initialize Zobrist hashing
        self.zobrist = ZobristHash(self.grid_size, self.num_shapes)
        self.memo = {}

        # For dead cell detection
        self.all_shape_masks = []
        for shape_idx in range(self.num_shapes):
            shape_masks = set()
            for orient_placements in self.placements[shape_idx]:
                shape_masks.update(orient_placements)
            self.all_shape_masks.append(shape_masks)

    def solve(self):
        """Main solving entry point."""
        grid_mask = 0  # 0 = all empty
        return self._backtrack(grid_mask, self.counts)

    def _backtrack(self, grid_mask, counts):
        """Recursive backtracking with memoization."""
        # Check memoization
        state_hash = self.zobrist.hash_state(grid_mask, counts)
        if state_hash in self.memo:
            return self.memo[state_hash]

        # If all shapes placed, success
        if all(c == 0 for c in counts):
            self.memo[state_hash] = True
            return True

        # Find first empty cell (Most Constrained Variable heuristic)
        empty_pos = self._find_best_empty(grid_mask)
        if empty_pos is None:
            self.memo[state_hash] = False
            return False

        # Try shapes in order
        for shape_idx in self.shape_order:
            if counts[shape_idx] == 0:
                continue

            # For each orientation
            for orient_idx, placements in enumerate(self.placements[shape_idx]):
                # Try each placement that covers the empty cell
                placement_mask = 1 << empty_pos
                for shape_mask in placements:
                    if shape_mask & placement_mask:  # This placement covers our empty cell
                        if (grid_mask & shape_mask) == 0:  # No overlap
                            # Place shape
                            new_grid_mask = grid_mask | shape_mask
                            new_counts = counts[:]
                            new_counts[shape_idx] -= 1

                            # Dead cell check: if any cell becomes impossible to fill, prune
                            if self._dead_cell_check(new_grid_mask, new_counts):
                                continue

                            if self._backtrack(new_grid_mask, new_counts):
                                self.memo[state_hash] = True
                                return True

        self.memo[state_hash] = False
        return False

    def _find_best_empty(self, grid_mask):
        """Find the most constrained empty cell (fewest possible shapes can fit)."""
        best_pos = None
        best_score = float('inf')

        # Try all empty positions
        for pos in range(self.grid_size):
            if not (grid_mask >> pos) & 1:  # Empty
                # Count how many shapes (with remaining counts) can cover this cell
                score = 0
                for shape_idx in range(self.num_shapes):
                    if self.counts[shape_idx] > 0:
                        for shape_mask in self.all_shape_masks[shape_idx]:
                            if (shape_mask >> pos) & 1:
                                if (grid_mask & shape_mask) == 0:
                                    score += 1
                                    break

                if score < best_score:
                    best_score = score
                    best_pos = pos
                    if score == 0:  # Dead cell
                        return pos

        return best_pos

    def _dead_cell_check(self, grid_mask, counts):
        """Check if any empty cell cannot be filled by any remaining shape."""
        # For each empty cell
        for pos in range(self.grid_size):
            if not (grid_mask >> pos) & 1:  # Empty
                can_fill = False
                for shape_idx in range(self.num_shapes):
                    if counts[shape_idx] > 0:
                        for shape_mask in self.all_shape_masks[shape_idx]:
                            if (shape_mask >> pos) & 1:
                                if (grid_mask & shape_mask) == 0:
                                    can_fill = True
                                    break
                    if can_fill:
                        break
                if not can_fill:
                    return True  # Dead cell found
        return False


# ------------------------------------------------------------
# 6. Main solver
# ------------------------------------------------------------
def solve():
    # Read input
    with open('day12_input.txt', 'r') as f:
        lines = f.readlines()

    # Parse
    shapes, regions = parse_input(lines)

    # Count successful regions
    successful = 0
    results = []

    start_time = time.time()

    for region_idx, (w, h, counts) in enumerate(regions):
        solver = PackingSolver(shapes, w, h, counts)

        if solver.solve():
            successful += 1
            results.append(f"{w}x{h}: {' '.join(map(str, counts))} -> fits")
        else:
            results.append(f"{w}x{h}: {' '.join(map(str, counts))} -> no fit")

        # Progress indicator
        if (region_idx + 1) % 10 == 0:
            print(f"Processed {region_idx + 1}/{len(regions)} regions...")

    total_time = time.time() - start_time

    # Write output
    with open('day12_output.txt', 'w') as f:
        f.write(f"Total regions that fit: {successful}\n")
        f.write(f"Time: {total_time:.2f} seconds\n")
        for r in results:
            f.write(r + "\n")

    print(f"\nTotal regions that fit: {successful}")
    print(f"Time: {total_time:.2f} seconds")


if __name__ == '__main__':
    solve()