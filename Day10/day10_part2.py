import re
from z3 import Int, Optimize, Sum, sat


def parse_line(line):
    # Example: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    # Ignore the [...] part
    first_bracket = line.find(']')
    rest = line[first_bracket + 1:].strip()

    # Buttons are in parentheses
    buttons = []
    button_pattern = r'\(([^)]+)\)'
    for match in re.finditer(button_pattern, rest):
        content = match.group(1)
        if content:
            indices = tuple(map(int, content.split(',')))
            buttons.append(indices)
        else:
            buttons.append(())  # empty button, probably not in input

    # Targets are in curly braces
    target_match = re.search(r'\{([^}]+)\}', rest)
    targets = list(map(int, target_match.group(1).split(',')))

    return buttons, targets


def solve_machine(buttons, targets):
    n_buttons = len(buttons)
    m_counters = len(targets)

    # Create variables
    presses = [Int(f'x_{i}') for i in range(n_buttons)]
    opt = Optimize()

    # Non-negativity
    for p in presses:
        opt.add(p >= 0)

    # For each counter, sum of presses for buttons affecting it == target
    for i in range(m_counters):
        total = 0
        for j in range(n_buttons):
            if i in buttons[j]:
                total += presses[j]
        opt.add(total == targets[i])

    # Minimize total presses
    total_presses = Sum(presses)
    opt.minimize(total_presses)

    if opt.check() == sat:
        model = opt.model()
        total = sum(model[p].as_long() for p in presses)
        return total
    else:
        raise Exception("Unsatisfiable")


def main():
    total_presses = 0
    with open('day10_input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            buttons, targets = parse_line(line)
            min_presses = solve_machine(buttons, targets)
            total_presses += min_presses

    print("Total fewest presses:", total_presses)


if __name__ == "__main__":
    main()