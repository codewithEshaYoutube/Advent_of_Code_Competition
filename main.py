# Advent of Code 2025 - Day 1 Solution
# Reads from input.txt and writes result to output.txt

def count_zero_hits(rotations, start=50):
    pos = start % 100
    zero_count = 0

    for line in rotations:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        steps = int(line[1:])

        if direction == 'L':
            pos = (pos - steps) % 100
        else:  # direction == 'R'
            pos = (pos + steps) % 100

        if pos == 0:
            zero_count += 1

    return zero_count


# --- Read input file ---
with open("input.txt", "r") as f:
    lines = f.readlines()

# --- Compute answer ---
answer = count_zero_hits(lines)

# --- Write output file ---
with open("output.txt", "w") as f:
    f.write(str(answer))

print("Password saved to output.txt:", answer)
