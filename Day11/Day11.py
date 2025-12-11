import sys
from collections import defaultdict


def count_paths(node, target, graph, memo):
    if node in memo:
        return memo[node]
    if node == target:
        return 1
    if node not in graph or not graph[node]:
        return 0

    total = 0
    for neighbor in graph[node]:
        total += count_paths(neighbor, target, graph, memo)

    memo[node] = total
    return total


def main():
    graph = defaultdict(list)

    # Try to read from file first, then stdin
    try:
        with open('day11_input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                node = parts[0].strip()
                outputs = [n.strip() for n in parts[1].split()]
                graph[node] = outputs
        print("Read from day11_input.txt")
    except FileNotFoundError:
        print("No day11_input.txt found, reading from stdin...")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            node = parts[0].strip()
            outputs = [n.strip() for n in parts[1].split()]
            graph[node] = outputs

    start = "you"
    end = "out"
    memo = {}
    result = count_paths(start, end, graph, memo)
    print(f"Number of paths from '{start}' to '{end}': {result}")


if __name__ == "__main__":
    main()