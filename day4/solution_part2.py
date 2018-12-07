from typing import Dict, Tuple

from day4.solution import (
    test_input_sorted, test_input_unsorted, get_guards,
    Guard
)


def find_guard_most_asleep_same_minute(guards: Dict[int, Guard]) -> Tuple[int, int, int]:
    """Given all Guards, find the one that was most asleep on the same minute.
    Return a tuple of its ID, the minute slept the most, and the count.
    """
    data = []
    for _id, guard in guards.items():
        _, most_occurring, occurrences = guard.calculate_sleep()
        data.append((_id, most_occurring, occurrences))
    return max(data, key=lambda item: item[2])


def test():
    lines = test_input_sorted.splitlines()
    guards = get_guards(lines)
    guard_id, most_occurring, occurrences = find_guard_most_asleep_same_minute(guards)
    print(f'[test] Which guard is most asleep the same minute: {guard_id}')
    assert guard_id == 99
    print(f'[test] Which minute does he sleep the most: {most_occurring}')
    assert most_occurring == 45
    print(f'[test] Solution - guard multiplied by minute: {guard_id * most_occurring}')

    lines = test_input_unsorted.splitlines()
    assert find_guard_most_asleep_same_minute(get_guards(lines)) == (guard_id, most_occurring, occurrences)
    print(f'[test] Verified sorted vs unsorted')


def solve():
    with open('input.txt') as f:
        lines = f.readlines()
    guards = get_guards(lines)
    guard_id, most_occurring, occurrences = find_guard_most_asleep_same_minute(guards)
    print(f'Which guard is most asleep the same minute: {guard_id}')
    print(f'Which minute does he sleep the most: {most_occurring}')
    print(f'Solution - guard multiplied by minute: {guard_id * most_occurring}')


if __name__ == '__main__':
    test()
    solve()
