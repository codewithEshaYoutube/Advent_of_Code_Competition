def day08():
    part = [0, 0]

    # Read input from the file
    with open('day8_input.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse boxes
    boxes = []
    for line in lines:
        parts = line.split(',')
        boxes.append([int(parts[0]), int(parts[1]), int(parts[2])])

    nboxes = len(boxes)
    print(f"Number of boxes: {nboxes}")

    # Calculate all pairwise squared distances
    print("Calculating distances...")
    distances = []
    for b1 in range(nboxes - 1):
        for b2 in range(b1 + 1, nboxes):
            dist = 0
            for i in range(3):
                dist += (boxes[b1][i] - boxes[b2][i]) ** 2
            distances.append(((b1 + 1, b2 + 1), dist))  # Julia uses 1-based indexing

    # Sort by distance
    print("Sorting distances...")
    workpairs = sorted(distances, key=lambda x: x[1])

    # Convert to list for easier popping (like Julia's popfirst!)
    workpairs_list = list(workpairs)

    used = set()
    circuits = []  # List of sets

    print("Processing connections...")
    connection_count = 0

    while workpairs_list:
        connection_count += 1
        (a, b), dist = workpairs_list.pop(0)  # popfirst!

        # Convert to 0-based for Python
        a -= 1
        b -= 1

        if a in used and b in used:
            # Find circuits containing a and b
            ca_idx = -1
            cb_idx = -1
            for i, circuit in enumerate(circuits):
                if a in circuit:
                    ca_idx = i
                if b in circuit:
                    cb_idx = i

            if ca_idx != cb_idx and ca_idx != -1 and cb_idx != -1:
                # Merge circuits
                circuits[ca_idx].update(circuits[cb_idx])
                circuits.pop(cb_idx)

                # Check if done (all boxes in one circuit)
                if len(circuits) == 1 and len(circuits[0]) == nboxes:
                    part[1] = boxes[a][0] * boxes[b][0]
                    print(f"Part 2: All boxes connected at connection {connection_count}")
                    print(f"  Box {a + 1} X: {boxes[a][0]}, Box {b + 1} X: {boxes[b][0]}")
                    print(f"  Product: {part[1]}")
                    break
        elif a in used:
            # Add b to circuit containing a
            for circuit in circuits:
                if a in circuit:
                    circuit.add(b)
                    break
        elif b in used:
            # Add a to circuit containing b
            for circuit in circuits:
                if b in circuit:
                    circuit.add(a)
                    break
        else:
            # Make new circuit
            circuits.append(set([a, b]))

        used.add(a)
        used.add(b)

        # Part 1: After 1000 connections
        if connection_count == 1000:
            # Sort circuits by size, get top 3
            circuits_sorted = sorted(circuits, key=len, reverse=True)
            if len(circuits_sorted) >= 3:
                part[0] = len(circuits_sorted[0]) * len(circuits_sorted[1]) * len(circuits_sorted[2])
            elif len(circuits_sorted) == 2:
                part[0] = len(circuits_sorted[0]) * len(circuits_sorted[1]) * 1
            elif len(circuits_sorted) == 1:
                part[0] = len(circuits_sorted[0]) * 1 * 1
            print(f"Part 1 after 1000 connections: {part[0]}")
            print(f"  Circuit sizes: {[len(c) for c in circuits_sorted[:5]]}")

    return part


# Run it
print("=" * 60)
print("Running Day 8 Solution (Julia-style)")
print("=" * 60)
result = day08()
print(f"\n✅ Final Results:")
print(f"  Part 1: {result[0]}")
print(f"  Part 2: {result[1]}")