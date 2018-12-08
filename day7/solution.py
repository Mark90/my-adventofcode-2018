import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List

test_instructions = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


@dataclass
class Step:
    complete: bool = False
    name: str = field(default_factory=str)
    requires: List['Step'] = field(default_factory=list)

    def available(self):
        return not any(step for step in self.requires if not step.complete)


def find_order_for_instructions(instructions: List[str]) -> str:
    """Process each instruction into 2 Step objects.
    Give each Step object a list of its required Steps.
    Then iteratively loop over the remaining Steps, find the first available and
    alphabetically lowest, complete it and add to steps done."""
    regex = r'Step (.) must be finished before step (.) can begin.'
    remaining = defaultdict(Step)
    for instruction in instructions:
        step_from, step_to = re.match(regex, instruction).groups()
        remaining[step_from].name = step_from
        remaining[step_to].name = step_to
        remaining[step_to].requires.append(remaining[step_from])

    done = []
    while remaining:
        available = (step for step in remaining.values() if step.available())
        step = sorted(available, key=lambda step: step.name)[0]
        step.complete = True
        done.append(step)
        del remaining[step.name]

    return ''.join(step.name for step in done)


def test():
    instructions = test_instructions.splitlines()
    order = find_order_for_instructions(instructions)
    print(f'[test] In what order should the steps be completed: {order}')
    assert order == 'CABDFE'


def solve():
    with open('input.txt') as f:
        instructions = f.readlines()
    order = find_order_for_instructions(instructions)
    print(f'In what order should the steps be completed: {order}')


if __name__ == '__main__':
    test()
    solve()
