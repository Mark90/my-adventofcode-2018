import re
import string
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Tuple

test_instructions = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

STEP_TIME = {
    v: k for k, v in enumerate(string.ascii_uppercase, 1)
}


@dataclass
class Step:
    complete: bool = False
    name: str = field(default_factory=str)
    requires: List['Step'] = field(default_factory=list)
    time_needed: int = 0
    time_started: int = None

    def start(self, time):
        self.time_started = time

    def available(self):
        return self.time_started is None and not any(step for step in self.requires if not step.complete)

    def ready(self, time):
        return (time - self.time_started) >= self.time_needed


@dataclass
class Worker:
    _id: int
    step: Step = None

    def available(self):
        return self.step is None

    def start(self, step: Step, time: int):
        step.start(time)
        self.step = step

    def ready(self, time):
        if self.step:
            return self.step.ready(time)

    def finish(self):
        step = self.step
        step.complete = True
        self.step = None
        return step


def get_steps(instructions, base_time):
    """Parse instructions to Steps, assign each one the required Steps and time to complete."""
    regex = r'Step (.) must be finished before step (.) can begin.'
    remaining = defaultdict(Step)
    for instruction in instructions:
        step_from, step_to = re.match(regex, instruction).groups()
        remaining[step_from].name = step_from
        remaining[step_from].time_needed = STEP_TIME[step_from] + base_time
        remaining[step_to].time_needed = STEP_TIME[step_to] + base_time
        remaining[step_to].name = step_to
        remaining[step_to].requires.append(remaining[step_from])
    return remaining


def calc_time_to_complete(instructions: List[str], base_time: int, workers: int) -> Tuple[str, int]:
    """Perform Steps by assigning them to Workers while incrementing the time.
    Repeat as long as there are remaining steps.
    Return the order in which Steps were completed and the total time taken."""
    remaining = get_steps(instructions, base_time)
    workers = [Worker(i) for i in range(workers)]
    done = []
    current_time = 0
    while True:
        # Check if any steps have completed
        for worker in workers:
            if worker.ready(current_time):
                step = worker.finish()
                done.append(step)
                del remaining[step.name]

        # Check if any remaining steps can be started
        available = (step for step in remaining.values() if step.available())
        for step in sorted(available, key=lambda x: x.name):
            for worker in workers:
                if worker.available():
                    worker.start(step, current_time)
                    break

        if not remaining:
            break
        current_time += 1

    return ''.join(step.name for step in done), current_time


def test():
    instructions = test_instructions.splitlines()
    base_time = 0
    workers = 2
    order, time = calc_time_to_complete(instructions, base_time, workers)
    print(f'[test] In what order should the steps be completed: {order}')
    print(f'[test] How much time will it take to complete the steps: {time}')
    assert order == 'CABFDE'
    assert time == 15


def solve():
    with open('input.txt') as f:
        instructions = f.readlines()
    base_time = 60
    workers = 5
    order, time = calc_time_to_complete(instructions, base_time, workers)
    print(f'In what order should the steps be completed: {order}')
    print(f'How much time will it take to complete the steps: {time}')


if __name__ == '__main__':
    test()
    solve()
