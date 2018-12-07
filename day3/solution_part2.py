import re
from collections import defaultdict, Counter
from typing import Tuple, List, Iterable, Dict


def generate_positions(claim: str) -> Iterable[Tuple]:
    """Given a claim, yield tuples of the (x, y) positions on the fabric."""
    match = re.match(r'#\d+ @ (\d+),(\d+): (\d+)x(\d+)', claim.strip())
    start_x, start_y, width, height = map(int, match.groups())
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            yield (x, y)


def info(claim: str) -> Tuple[int, int]:
    """Given a claim, return its ID and size"""
    match = re.match(r'#(\d+) @ \d+,\d+: (\d+)x(\d+)', claim.strip())
    claim_id, width, height = map(int, match.groups())
    return claim_id, width * height


def aggregate(claims: List[str]) -> Tuple[defaultdict, Dict]:
    """Given list of claims, return 2 dicts: one with the claims on each position,
    the other containing the size of each claim."""
    claims_on_position = defaultdict(list)
    claim_sizes = {}
    for claim in claims:
        claim_id, claim_size = info(claim)
        claim_sizes[claim_id] = claim_size
        for position in generate_positions(claim):
            claims_on_position[position].append(claim_id)
    return claims_on_position, claim_sizes


def test():
    claims_on_position, claim_sizes = aggregate(['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2'])
    unique_claim_positions = Counter((j[0] for j in claims_on_position.values() if len(j) == 1))
    unique_claims = [claim for claim, unique_count in unique_claim_positions.items()
                     if claim_sizes[claim] == unique_count]
    print('[test] What is the ID of the only claim that doesn\'t overlap:')
    print(unique_claims[0])
    assert unique_claims == [3]


def solve():
    with open('input.txt') as f:
        claims = f.readlines()
    claims_on_position, claim_sizes = aggregate(claims)
    unique_claim_positions = Counter((j[0] for j in claims_on_position.values() if len(j) == 1))
    unique_claims = [claim for claim, unique_count in unique_claim_positions.items()
                     if claim_sizes[claim] == unique_count]
    print('What is the ID of the only claim that doesn\'t overlap:')
    print(unique_claims[0])


if __name__ == '__main__':
    test()
    solve()
