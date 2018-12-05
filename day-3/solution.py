import re
from collections import defaultdict
from typing import Tuple, List, Iterable


def generate_positions(claim: str) -> Iterable[Tuple]:
    """Given a claim, yield tuples of the (x, y) positions on the fabric."""
    match = re.match(r'#\d+ @ (\d+),(\d+): (\d+)x(\d+)', claim.strip())
    start_x, start_y, width, height = map(int, match.groups())
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            yield (x, y)


def aggregate(claims: List[str]) -> defaultdict:
    """Given list of claims, return the total number of times each square inch was claimed."""
    total = defaultdict(int)
    for claim in claims:
        for position in generate_positions(claim):
            total[position] += 1
    return total


def test():
    counts = aggregate(['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2'])
    print('[test] How many square inches of fabric are within two or more claims:')
    result = len([v for v in counts.values() if v >= 2])
    print(result)
    assert result == 4


def solve():
    with open('input.txt') as f:
        claims = f.readlines()
    counts = aggregate(claims)
    print('How many square inches of fabric are within two or more claims:')
    print(len([v for v in counts.values() if v >= 2]))


if __name__ == '__main__':
    test()
    solve()
