def calculate_part2():
    with open('day8_input.txt', 'r') as f:
        boxes = []
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                boxes.append((x, y, z))

    n = len(boxes)
    print(f"Total boxes: {n}")

    # Calculate all distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = boxes[i][0] - boxes[j][0]
            dy = boxes[i][1] - boxes[j][1]
            dz = boxes[i][2] - boxes[j][2]
            dist_sq = dx * dx + dy * dy + dz * dz
            edges.append((dist_sq, i, j))

    edges.sort(key=lambda x: x[0])

    # Union-Find
    parent = list(range(n))
    rank = [0] * n
    size = [1] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x == root_y:
            return False

        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
            size[root_y] += size[root_x]
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
            size[root_x] += size[root_y]
        else:
            parent[root_y] = root_x
            size[root_x] += size[root_y]
            rank[root_x] += 1
        return True

    # Keep connecting until all boxes are in one circuit
    last_edge_boxes = None
    for i, (dist_sq, a, b) in enumerate(edges, 1):
        if union(a, b):
            # Check if all boxes are now connected
            root = find(0)
            all_connected = True
            for box in range(n):
                if find(box) != root:
                    all_connected = False
                    break

            if all_connected:
                last_edge_boxes = (a, b)
                print(f"All boxes connected after {i} connections")
                print(f"Last edge: boxes {a} and {b}")
                print(f"X coordinates: {boxes[a][0]} and {boxes[b][0]}")
                result = boxes[a][0] * boxes[b][0]
                print(f"Part 2 result: {result}")
                return result

    return 0


print("=" * 60)
print("Calculating Part 2")
print("=" * 60)
part2_result = calculate_part2()
print(f"\n✅ Part 2 Answer: {part2_result}")