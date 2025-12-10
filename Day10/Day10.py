def parse_line(line):
    import re
    bracket_part = re.search(r'\[(.*?)\]', line).group(1)
    target = [1 if ch == '#' else 0 for ch in bracket_part]
    n = len(target)
    buttons = []
    for match in re.findall(r'\(([\d,]+)\)', line):
        bt = [0]*n
        indices = map(int, match.split(','))
        for idx in indices:
            bt[idx] = 1
        buttons.append(bt)
    return target, buttons

def min_presses_for_machine(target, buttons):
    n = len(target)
    m = len(buttons)
    min_presses = float('inf')
    # Brute force subsets
    for mask in range(1 << m):
        presses = bin(mask).count('1')
        if presses >= min_presses:
            continue
        state = [0]*n
        for j in range(m):
            if mask >> j & 1:
                bt = buttons[j]
                for i in range(n):
                    if bt[i]:
                        state[i] ^= 1
        if state == target:
            min_presses = presses
    return min_presses

def solve(input_text):
    total = 0
    for line in input_text.strip().splitlines():
        target, buttons = parse_line(line)
        total += min_presses_for_machine(target, buttons)
    return total

# Read from day10_input.py
import os

# First check if file exists
if not os.path.exists('day10_input.py'):
    # Create file if it doesn't exist (for demonstration)
    # In real scenario, this would be your actual input
    sample_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    with open('day10_input.py', 'w') as f:
        f.write(sample_input)

# Read the file
with open('day10_input.py', 'r') as f:
    input_data = f.read()

result = solve(input_data)
print(f"Fewest button presses required: {result}")