import sys
from collections import defaultdict


def parse_input(filename="day11_input.txt"):
    """Parse input from a file."""
    graph = defaultdict(list)
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                node = parts[0].strip()
                outputs = [n.strip() for n in parts[1].split()]
                graph[node] = outputs
        print(f"✓ Successfully read {filename}")
        return graph
    except FileNotFoundError:
        print(f"✗ Error: {filename} not found!")
        print("\nMake sure:")
        print("1. The file 'day11_input.txt' exists in the same folder")
        print("2. You're running the script from the correct folder")
        return None


# ===== PART 1: Count paths from "you" to "out" =====
def count_paths_part1(graph):
    """Count all paths from 'you' to 'out'."""

    def dfs(node, memo):
        if node in memo:
            return memo[node]
        if node == "out":
            return 1
        if node not in graph or not graph[node]:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor, memo)

        memo[node] = total
        return total

    memo = {}
    return dfs("you", memo)


# ===== PART 2: Count paths from "svr" to "out" visiting both "dac" and "fft" =====
def count_paths_part2(graph):
    """Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""

    def dfs(node, visited_dac, visited_fft, memo):
        # Create memoization key
        memo_key = (node, visited_dac, visited_fft)
        if memo_key in memo:
            return memo[memo_key]

        # Update visited status
        has_dac = visited_dac or (node == "dac")
        has_fft = visited_fft or (node == "fft")

        # Reached target
        if node == "out":
            result = 1 if has_dac and has_fft else 0
            memo[memo_key] = result
            return result

        # Dead end
        if node not in graph or not graph[node]:
            memo[memo_key] = 0
            return 0

        # Explore neighbors
        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor, has_dac, has_fft, memo)

        memo[memo_key] = total
        return total

    memo = {}
    return dfs("svr", False, False, memo)


def main():
    # Read input
    graph = parse_input("day11_input.txt")
    if graph is None:
        return

    print("\n" + "=" * 50)
    print("DAY 11 REACTOR - PATH COUNTING")
    print("=" * 50)

    # Part 1
    print("\n--- PART 1 ---")
    print("Counting paths from 'you' to 'out'...")
    result1 = count_paths_part1(graph)
    print(f"✓ Number of paths: {result1}")

    # Part 2
    print("\n--- PART 2 ---")
    print("Counting paths from 'svr' to 'out' that visit both 'dac' and 'fft'...")
    result2 = count_paths_part2(graph)
    print(f"✓ Number of valid paths: {result2}")

    print("\n" + "=" * 50)
    print(f"PART 1 ANSWER: {result1}")
    print(f"PART 2 ANSWER: {result2}")
    print("=" * 50)


if __name__ == "__main__":
    main()