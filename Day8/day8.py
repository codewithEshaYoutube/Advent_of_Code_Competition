import math
import sys


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1

        return True


def solve_puzzle():
    # Read input
    try:
        with open("input_day8.txt", "r") as f:
            lines = f.read().strip().split('\n')
    except FileNotFoundError:
        print("Error: input_day8.txt not found!")
        sys.exit(1)

    # Parse coordinates
    coordinates = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(',')
            if len(parts) == 3:
                x, y, z = map(int, parts)
                coordinates.append((x, y, z))

    n = len(coordinates)
    print(f"Processing {n} junction boxes...")

    # Generate all pairs with distances
    print("Calculating distances for all pairs...")
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = coordinates[i][0] - coordinates[j][0]
            dy = coordinates[i][1] - coordinates[j][1]
            dz = coordinates[i][2] - coordinates[j][2]
            dist = dx * dx + dy * dy + dz * dz  # Use squared distance for comparison
            edges.append((dist, i, j))

    print(f"Sorting {len(edges)} edges...")
    edges.sort(key=lambda x: x[0])

    # Initialize Union-Find
    uf = UnionFind(n)

    # Make 1000 connections
    print("\nMaking 1000 connections...")
    connections_made = 0
    edges_processed = 0

    for dist, i, j in edges:
        edges_processed += 1
        if uf.union(i, j):
            connections_made += 1
            if connections_made % 100 == 0:
                print(f"  Connections made: {connections_made}")

        if connections_made >= 1000:
            break

    print(f"\nProcessed {edges_processed} edges to make {connections_made} connections")

    # Count component sizes
    print("Counting component sizes...")
    component_sizes = {}
    for i in range(n):
        root = uf.find(i)
        component_sizes[root] = component_sizes.get(root, 0) + 1

    sizes = list(component_sizes.values())
    sizes.sort(reverse=True)

    print(f"\nAfter 1000 connections:")
    print(f"Number of circuits: {len(sizes)}")
    print(f"Largest component sizes: {sizes[:5]}")

    # Calculate result
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
        print(f"\nThree largest: {sizes[0]}, {sizes[1]}, {sizes[2]}")
        print(f"Product = {result}")
    else:
        result = 0
        print("Error: Less than 3 components!")

    # Save result
    with open("output_day8.txt", "w") as f:
        f.write(str(result))

    print(f"\nResult saved to output_day8.txt")
    return result


if __name__ == "__main__":
    result = solve_puzzle()
    print(f"Final answer: {result}")