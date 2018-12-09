from dataclasses import dataclass
from itertools import islice
from typing import List, Iterable


@dataclass
class Node:
    children: List['Node']
    metadata: List[int]

    def value(self):
        if not self.children:
            return sum(self.metadata)
        return sum([self.children[i - 1].value() for i in self.metadata if i - 1 < len(self.children)])


def parse_nodes(numbers: Iterable[int]) -> Node:
    num_child, num_meta = islice(numbers, 2)
    children = [parse_nodes(numbers) for _ in range(num_child)]
    return Node(children, list(islice(numbers, num_meta)))


def test():
    license = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    numbers = map(int, license.strip().split(' '))
    tree = parse_nodes(numbers)
    value = tree.value()
    print(f'[test] The tree value is: {value}')
    assert value == 66


def solve():
    with open('input.txt') as f:
        license = f.read()
    numbers = map(int, license.strip().split(' '))
    tree = parse_nodes(numbers)
    value = tree.value()
    print(f'The tree value is: {value}')


if __name__ == '__main__':
    test()
    solve()
