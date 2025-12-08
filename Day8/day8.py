import math
import numpy as np
import networkx as nx
from itertools import combinations


def solve():
    # Read input from file
    with open("day8_input.txt", "r") as f:
        lines = f.readlines()

    # Parse coordinates
    input_data = []
    for line in lines:
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            input_data.append([x, y, z])

    input_data = np.array(input_data)
    n = len(input_data)

    # Part 1 ----
    print("Calculating distances...")

    # Calculate all pairwise distances
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.sqrt(((input_data[i] - input_data[j]) ** 2).sum())
            distances[i, j] = dist
            distances[j, i] = dist

    # Set diagonal to infinity
    np.fill_diagonal(distances, np.inf)

    # Get all pairs (upper triangle)
    pairs = []
    dist_list = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((i, j))
            dist_list.append(distances[i, j])

    # Sort pairs by distance
    sorted_indices = np.argsort(dist_list)
    ordered_pairs = [pairs[i] for i in sorted_indices]

    # Take first 1000 edges
    edges = ordered_pairs[:1000]

    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Get connected components
    comp = list(nx.connected_components(G))
    comp_sizes = [len(c) for c in comp]
    comp_sizes.sort(reverse=True)

    solution1 = comp_sizes[0] * comp_sizes[1] * comp_sizes[2]
    print(f"Part 1 Solution: {solution1}")

    # Part 2 ----
    print("\nStarting Part 2...")

    i = 1001
    edges = ordered_pairs[:i]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    comp = list(nx.connected_components(G))
    comp_sizes = [len(c) for c in comp]

    while len(set(comp_sizes)) > 1:
        i += 1
        edges = ordered_pairs[:i]
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        comp = list(nx.connected_components(G))
        comp_sizes = [len(c) for c in comp]

    # Get the last edge that was added
    last_edge = ordered_pairs[i - 1]
    solution2 = input_data[last_edge[0], 0] * input_data[last_edge[1], 0]

    print(f"Part 2 Solution: {solution2}")
    print(f"Last edge: {last_edge}")
    print(f"X coordinates: {input_data[last_edge[0], 0]}, {input_data[last_edge[1], 0]}")

    return solution1, solution2


if __name__ == "__main__":
    s1, s2 = solve()
    print(f"\nPart 1 Answer: {s1}")
    print(f"Part 2 Answer: {s2}")