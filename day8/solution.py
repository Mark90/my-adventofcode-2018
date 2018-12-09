from dataclasses import dataclass
from itertools import islice
from typing import List, Iterable


@dataclass
class Node:
    children: List['Node']
    metadata: List[int]

    def sum_of_metadata(self) -> int:
        return sum(self.metadata) + sum(child.sum_of_metadata() for child in self.children)


def parse_nodes(numbers: Iterable[int]) -> Node:
    num_child, num_meta = islice(numbers, 2)
    children = [parse_nodes(numbers) for _ in range(num_child)]
    return Node(children, list(islice(numbers, num_meta)))


def test():
    license = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    numbers = map(int, license.strip().split(' '))
    tree = parse_nodes(numbers)
    sum_of_metadata = tree.sum_of_metadata()
    print(f'[test] The sum of metadata entries is: {sum_of_metadata}')
    assert sum_of_metadata == 138


def solve():
    with open('input.txt') as f:
        license = f.read()
    numbers = map(int, license.strip().split(' '))
    tree = parse_nodes(numbers)
    sum_of_metadata = tree.sum_of_metadata()
    print(f'The sum of metadata entries is: {sum_of_metadata}')


if __name__ == '__main__':
    test()
    solve()
