def max_joltage(line):
    """Return the maximum two-digit number formed by two positions i < j in line."""
    max_val = -1
    n = len(line)
    for i in range(n):
        a = int(line[i])
        for j in range(i + 1, n):
            b = int(line[j])
            val = 10 * a + b
            if val > max_val:
                max_val = val
    return max_val


def solve():
    total = 0
    lines = []

    # Parse the input - it appears to be one continuous block
    input_text = """4346343235149456543445233353534244533333333343433259333326337334334333438332533343452433223352443324
    2323233732423333335633333322134234324554233323746324333322454233432477323332532436412434167322334333
    ... [rest of input truncated for display]"""

    # Actually, let me read from the actual input file
    with open("day3_input.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []
    for line in lines:
        val = max_joltage(line)
        results.append(val)
        total += val

    with open("day3_output.txt.txt", "w") as out:
        out.write(str(total))

    print(f"Total output joltage: {total}")
    return total


if __name__ == "__main__":
    solve()