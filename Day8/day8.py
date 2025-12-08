import math


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

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


def main():
    # Read input
    with open("day8_input.txt", "r") as f:
        coords = [tuple(map(int, line.strip().split(',')))
                  for line in f if line.strip()]

    n = len(coords)

    # Generate and sort edges by squared distance
    edges = []
    for i in range(n):
        xi, yi, zi = coords[i]
        for j in range(i + 1, n):
            xj, yj, zj = coords[j]
            dist_sq = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            edges.append((dist_sq, i, j))

    edges.sort(key=lambda x: x[0])

    # Union-Find
    uf = UnionFind(n)
    connections = 0

    for _, i, j in edges:
        if uf.union(i, j):
            connections += 1
            if connections == 1000:
                break

    # Get component sizes
    comp_sizes = {}
    for i in range(n):
        root = uf.find(i)
        comp_sizes[root] = comp_sizes.get(root, 0) + 1

    sizes = sorted(comp_sizes.values(), reverse=True)
    result = sizes[0] * sizes[1] * sizes[2]

    # Save result
    with open("day8_output.txt", "w") as f:
        f.write(str(result))

    return result


if __name__ == "__main__":
    answer = main()
    print(f"Answer: {answer}")