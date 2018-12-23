"""
Part1: ~75ms
Part2: ~3500ms

Python 3.7, Intel i5 7200u
"""
import itertools
import time
from functools import lru_cache


@lru_cache(maxsize=4 * 1024)
def row_above(xx, yy, width):
    return ((yy - 1) * width) + xx


@lru_cache(maxsize=4 * 1024)
def row_middle(xx, yy, width):
    return (yy * width) + xx


@lru_cache(maxsize=4 * 1024)
def row_below(xx, yy, width):
    return ((yy + 1) * width) + xx


@lru_cache(maxsize=8 * 1024)
def split_chars(string):
    return string[4], ''.join(sorted(string[0:4] + string[5:]))


adjacent_acre_combinations = list(''.join(c) for c in itertools.combinations_with_replacement(sorted('#.|'), 8))

acre_transitions = {
    '.': {c: ('|' if c.count('|') > 2 else '.') for c in adjacent_acre_combinations},
    '|': {c: ('#' if c.count('#') > 2 else '|') for c in adjacent_acre_combinations},
    '#': {c: ('#' if ('#' in c and '|' in c) else '.') for c in adjacent_acre_combinations},
}


def deforest(real_acres, real_width, real_height, total_minutes):
    """Add empty acres as 'padding' forest to keep edgecases easy, and ignore
    them in the resulting forest.

    Check for recurring composition of all acres. When one is found, 'fast-forward' time
    a multiple of the minutes passed since the previous occurrence.
    """
    padded_width = real_width + 2
    y_padding = '.' * padded_width

    curr_minute = 0
    resource_value = 0
    forwarded_minutes = False
    acres_seen = {}
    while curr_minute < total_minutes:
        if not forwarded_minutes:
            if real_acres in acres_seen:
                delta = curr_minute - acres_seen[real_acres]
                new_minute = curr_minute + (((total_minutes - curr_minute) // delta) * delta)
                # print(f'Fast-forward from minute {curr_minute} to {new_minute}')
                forwarded_minutes = True
                curr_minute = new_minute
                if curr_minute == total_minutes:
                    break
            acres_seen[real_acres] = curr_minute

        padded_acres = f'{y_padding}' + ''.join(f'.{line}.' for line in real_acres.splitlines()) + f'{y_padding}'
        new_acres = ''
        for y in range(1, real_width + 1):
            for x in range(1, real_height + 1):
                # super inefficient way to get the get the 9 adjacent_acres
                adjacent_acres = padded_acres[row_above(x, y, padded_width) - 1:row_above(x, y, padded_width) + 2]
                adjacent_acres += padded_acres[row_middle(x, y, padded_width) - 1:row_middle(x, y, padded_width) + 2]
                adjacent_acres += padded_acres[row_below(x, y, padded_width) - 1:row_below(x, y, padded_width) + 2]

                # split middle char from it and get the other 8 adjacent_acres sorted
                cur_acre, surrounding_acres = split_chars(adjacent_acres)
                new_acre = acre_transitions[cur_acre][surrounding_acres]
                new_acres += new_acre
            new_acres += '\n'
        real_acres = new_acres
        curr_minute += 1
        resource_value = real_acres.count('#') * real_acres.count('|')
    return resource_value


def test_part1():
    field = (".#.#...|#.\n.....#|##|\n.|..|...#.\n..|#.....#\n#.#|||#|#|\n...#.||...\n.|....|...\n"
             "||...#|.#|\n|.||||..|.\n...#.|..|.\n")
    lines = [i.strip() for i in field.splitlines() if i.strip()]
    real_width, real_height = len(lines[0]), len(lines)
    acres = ''.join(f'{line}\n' for line in lines)

    t_start = time.time()
    final_resource_value = deforest(acres, real_width, real_height, 10)
    t_taken = (time.time() - t_start) * 1000
    print(f'Test part 1: found solution {final_resource_value} after {t_taken:.3f}ms')


def solve_part1():
    raw = open('input.txt').read()
    lines = [i.strip() for i in raw.splitlines() if i.strip()]
    real_width, real_height = len(lines[0]), len(lines)
    acres = ''.join(f'{line}\n' for line in lines)

    t_start = time.time()
    final_resource_value = deforest(acres, real_width, real_height, 10)
    t_taken = (time.time() - t_start) * 1000
    print(f'Part 1: found solution {final_resource_value} after {t_taken:.3f}ms')


def solve_part2():
    raw = open('input.txt').read()
    lines = [i.strip() for i in raw.splitlines() if i.strip()]
    real_width, real_height = len(lines[0]), len(lines)
    acres = ''.join(f'{line}\n' for line in lines)

    t_start = time.time()
    final_resource_value = deforest(acres, real_width, real_height, 1_000_000_000)
    t_taken = (time.time() - t_start) * 1000
    print(f'Part 2: found solution {final_resource_value} after {t_taken:.3f}ms')


if __name__ == '__main__':
    test_part1()
    solve_part1()
    solve_part2()
