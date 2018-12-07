"""Had to try out dataclasses."""
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple, List, Dict

test_input_sorted = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

test_input_unsorted = """[1518-11-01 00:05] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-01 00:55] wakes up
[1518-11-04 00:46] wakes up
[1518-11-02 00:40] falls asleep
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-01 00:30] falls asleep
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-02 00:50] wakes up
[1518-11-01 00:25] wakes up
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-04 00:36] falls asleep
[1518-11-05 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-05 00:45] falls asleep"""


@dataclass
class Event:
    when: datetime
    wake: bool
    sleep: bool
    start_shift: bool
    guard_id: int = None


@dataclass
class Guard:
    events: List[Event] = field(default_factory=list)

    def calculate_sleep(self) -> Tuple[int, int, int]:
        """Loop through this guard's events.
        Return how many minutes he slept,
        which minute he was asleep the most
        and the occurrences of that minute."""
        if not self.events:
            return 0, 0, 0

        seconds = 0
        minute_occurrences = defaultdict(int)

        asleep_since = None
        for event in self.events:
            if event.wake:
                awoke = event.when
                seconds += (awoke - asleep_since).total_seconds()
                for minute in range(asleep_since.minute, awoke.minute):
                    minute_occurrences[minute] += 1

            if event.sleep:
                asleep_since = event.when

        minutes = seconds // 60
        most_occurring = max(minute_occurrences.items(), key=lambda minute_and_count: minute_and_count[1])
        return minutes, most_occurring[0], most_occurring[1]


def find_sleepiest_guard(guards: Dict[int, Guard]) -> Tuple[int, int, int]:
    """Given all Guards, find the one that slept the most.
    Return a tuple of its ID, the total minutes, and the most occurring minute.
    """
    data = []
    for _id, guard in guards.items():
        minutes, most_occurring, _ = guard.calculate_sleep()
        data.append((_id, minutes, most_occurring))
    return max(data, key=lambda item: item[1])


def create_event(line: str) -> Event:
    """Parse a line into an Event."""
    timestamp, text = line.strip().split('] ')
    when = datetime.strptime(timestamp, '[%Y-%m-%d %H:%M')
    match_shift_start = re.match(r'Guard #(\d+) begins shift', text)
    if match_shift_start:
        return Event(when, False, False, True, int(match_shift_start.group(1)))
    return Event(when, text == 'wakes up', text == 'falls asleep', False)


def get_guards(lines: List[str]) -> Dict[int, Guard]:
    """Parse all lines into Events.
    Loop over Events sorted by time,
    and add them to their corresponding Guard."""
    guards = defaultdict(Guard)

    current_guard = None
    for event in sorted((create_event(line) for line in lines), key=lambda evt: evt.when):
        if event.start_shift:
            current_guard = event.guard_id
        else:
            guards[current_guard].events.append(event)

    return guards


def test():
    lines = test_input_sorted.splitlines()
    guards = get_guards(lines)
    guard_id, minutes, most_occurring = find_sleepiest_guard(guards)
    print(f'[test] Which guard sleeps the most: {guard_id}')
    assert guard_id == 10
    print(f'[test] Which minute does he sleep the most: {most_occurring}')
    assert most_occurring == 24
    print(f'[test] Solution - guard multiplied by minute: {guard_id * most_occurring}')

    lines = test_input_unsorted.splitlines()
    assert find_sleepiest_guard(get_guards(lines)) == (guard_id, minutes, most_occurring)
    print(f'[test] Verified sorted vs unsorted')


def solve():
    with open('input.txt') as f:
        lines = f.readlines()
    guards = get_guards(lines)
    guard_id, minutes, most_occurring = find_sleepiest_guard(guards)
    print(f'Which guard sleeps the most: {guard_id}')
    print(f'Which minute does he sleep the most: {most_occurring}')
    print(f'Solution - guard multiplied by minute: {guard_id * most_occurring}')


if __name__ == '__main__':
    test()
    solve()
