"""~300ms part1+part2, Python 3.7"""
import time
from collections import defaultdict, namedtuple
from typing import Dict, Callable

from day20.data import examples

Coord = namedtuple('Coord', 'x y')


def up_from(coord: 'Coord'):
    return Coord(coord.x, coord.y - 1)


def down_from(coord: 'Coord'):
    return Coord(coord.x, coord.y + 1)


def left_from(coord: 'Coord'):
    return Coord(coord.x - 1, coord.y)


def right_from(coord: 'Coord'):
    return Coord(coord.x + 1, coord.y)


translate_char = {
    'N': (up_from, '-'),
    'E': (right_from, '|'),
    'S': (down_from, '-'),
    'W': (left_from, '|'),
}


def get_field_for_regex(regular_expression: str):
    grid = defaultdict(lambda: defaultdict(lambda: '#'))
    start = Coord(0, 0)
    grid[start.x][start.y] = 'X'

    def parse(cur: Coord, line: str, idx=0) -> int:
        orig_cur = cur
        while idx < len(line):
            char = line[idx]
            idx += 1
            if char == '(':
                idx = parse(cur, line, idx=idx)
                continue
            if char == '|':
                cur = orig_cur
                continue
            if char == ')':
                return idx
            next_position, door_symbol = translate_char[char]
            door = next_position(cur)
            room = next_position(door)
            cur = room
            grid[door.x][door.y] = door_symbol
            grid[room.x][room.y] = '.'
        return idx

    parse(start, regular_expression)
    return grid


def visit(field: Dict, node: Coord, move_from: Callable):
    door_or_wall = move_from(node)
    if field[door_or_wall.x][door_or_wall.y] == '#':
        return
    return move_from(door_or_wall)


def bfs(field):
    distances = {}
    directions = (up_from, right_from, down_from, left_from)
    to_visit = [visit(field, Coord(0, 0), direction) for direction in directions]
    next_to_visit = []
    distance = 0
    while to_visit:
        distance += 1
        for node in to_visit:
            if not node or node in distances:
                continue
            distances[node] = distance
            next_to_visit.extend([visit(field, node, func) for func in directions])
        to_visit = next_to_visit
        next_to_visit = []
    return distances


def longest_shortest_path(field):
    shortest_path_to_each_room = bfs(field)
    return max(distance_to for room, distance_to in shortest_path_to_each_room.items())


def num_shortest_paths(field, length):
    shortest_path_to_each_room = bfs(field)
    return len([distance_to for room, distance_to in shortest_path_to_each_room.items() if distance_to >= length])


def test():
    for example in examples:
        field = get_field_for_regex(example['reg'])
        longest = longest_shortest_path(field)
        print(f'[test] {example["reg"]} Longest shortest-path ({example["longestpath"]}): {longest}')


def part1_part2():
    t_start = time.time()
    with open('input.txt') as f:
        regular_expression = f.read().replace('^', '').replace('$', '').strip()
    field = get_field_for_regex(regular_expression)
    longest = longest_shortest_path(field)
    count = num_shortest_paths(field, 1000)
    t_taken = (time.time() - t_start) * 1000.0
    print(f'[part1] Longest shortest-path: {longest}')
    print(f'[part2] Number of paths longer than 1000: {count}')
    print(f'{t_taken:.2f}ms for part 1 and 2')


if __name__ == '__main__':
    test()
    part1_part2()
