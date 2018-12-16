"""Crappy implementation (and not even completely correct).
Part2 is correct and done better (IMHO)
Needed a refresher course on bitwise operations, this one took me ~2h.
"""

m = {
    '#': '1',
    '.': '0',
}
mi = {v: k for k, v in m.items()}


def state_to_binary(s):
    return int(''.join(m[c] for c in s), 2)


def binary_to_state(s):
    return ''.join(mi[c] for c in bin(s)[2:])


initial_state = '##.#..#.#..#.####.#########.#...#.#.#......##.#.#...##.....#...#...#.##.#...##...#.####.##..#.#..#.'
init = state_to_binary(initial_state)

combinations_continue = [state_to_binary(comb) for comb in [
    '.#.#.',
    '.#...',
    '#####',
    '#..#.',
    '#...#',
    '###.#',
    '...##',
    '#.##.',
    '.#.##',
    '##.#.',
    '..###',
    '###..',
    '##..#',
    '#..##',
]]

combinations_empty = [state_to_binary(s) for s in [
    '..#..',
    '..#.#',
    '#.#..',
    '.#..#',
    '#....',
    '....#',
    '#.###',
    '####.',
    '.....',
    '.####',
    '.###.',
    '...#.',
    '##...',
    '..##.',
    '.##.#',
    '##.##',
    '.##..',
    '#.#.#',
]]


def highest_bit(number):
    return len(bin(number)[2:]) - 1


offset = (2 * len(combinations_continue)) + 2
curstate = init << offset  # make sure we'll never grow out of lower bound
initial_length = len(bin(curstate))

gone_left = 0

for t in range(20):
    print(f'{binary_to_state(curstate):.>70}')
    nextstate = curstate
    for pot in range(2, highest_bit(curstate) + 3):
        shiftleft = pot - 2
        for comb in combinations_continue:  # check each of the combinations that warrant a plant in the next gen
            comb = comb << shiftleft
            pot_surroundings = sum(curstate & (2 ** x) for x in range(pot - 2, pot + 3))
            if (comb ^ pot_surroundings) == 0:  # if this pot and the surroundoing ones match the state
                nextstate |= 2 ** pot  # add this pot to the next state
                break
        for comb in combinations_empty:  # check each of the combinations that prohibit a plant in the next gen
            comb = comb << shiftleft
            pot_surroundings = sum(curstate & (2 ** x) for x in range(pot - 2, pot + 3))
            if (comb ^ pot_surroundings) == 0:  # if this pot and the surroundoing ones match the state
                before = nextstate
                nextstate &= ~(2 ** pot)  # remove this pot from next state
                break
    curstate = nextstate

print('DONE')
print(f'{binary_to_state(curstate):.>70}')

after_length = len(bin(curstate))
gone_left = after_length - initial_length

s = 0
print(curstate)
print(binary_to_state(curstate))
for idx, value in enumerate(binary_to_state(curstate)):
    if value == '#':
        s += (idx - gone_left)
print('SUM:', s)
