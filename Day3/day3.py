def max_12_digit_joltage(line):
    """Return the maximum 12-digit number formed by selecting 12 positions i1 < i2 < ... < i12."""
    n = len(line)
    k = 12  # number of digits we need to keep
    to_remove = n - k

    stack = []
    for digit in line:
        while to_remove > 0 and stack and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # If we still have digits to remove, remove from the end
    if to_remove > 0:
        stack = stack[:-to_remove]

    # Take exactly k digits (should be exactly 12)
    result = ''.join(stack[:k])
    return int(result)


def solve_part2():
    total = 0
    # Read input
    with open("day3_input.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []
    for line in lines:
        val = max_12_digit_joltage(line)
        results.append(val)
        total += val

    with open("day3_OUTPUT.txt", "w") as out:
        out.write(str(total))

    print(f"Total output joltage (Part 2): {total}")
    return total


if __name__ == "__main__":
    solve_part2()