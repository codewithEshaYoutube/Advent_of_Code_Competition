def solve():
    with open("input.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    dial = 50
    count_zero = 0

    for line in lines:
        direction = line[0]
        steps = int(line[1:])

        # Each single click
        for _ in range(steps):
            if direction == 'L':
                dial = (dial - 1) % 100
            else:
                dial = (dial + 1) % 100

            if dial == 0:
                count_zero += 1

    # Save result to output.txt
    with open("output.txt", "w") as f:
        f.write(str(count_zero))


if __name__ == "__main__":
    solve()
