"""Water settling algorithm. Fun challenge.

Algorithm is pretty simplistic, but performance was not really a factor here.
Took 5h to solve both parts, stuck on an off-by-one problem for a while. Another 2h for clean-ish code.

~47s on Python 3.7, intel i7 870.
"""
import re
import time
from typing import Tuple, Set

t_start = time.time()


def up_from(coord):
    return coord[0], coord[1] - 1


def down_from(coord):
    return coord[0], coord[1] + 1


def left_from(coord):
    return coord[0] - 1, coord[1]


def right_from(coord):
    return coord[0] + 1, coord[1]


class NorthPole:
    clay: Set[Tuple[int, int]] = set()  # All clay blocks
    settled: Set[Tuple[int, int]] = set()  # Settled water blocks
    reachable: Set[Tuple[int, int]] = set()  # Sand blocks reachable by water

    def __init__(self, slices):
        self.slices = slices
        self.xmin = min((i for slice in slices for i in slice['x']))
        self.xmax = max((i for slice in slices for i in slice['x']))
        self.ymin = min((i for slice in slices for i in slice['y']))
        self.ymax = max((i for slice in slices for i in slice['y']))
        self.clay = set([(x, y) for item in slices for x in item['x'] for y in item['y']])

    def debug_grid(self):
        grid = {y: tuple(x for item in self.slices for x in item['x'] if y in item['y'])
                for y in range(0, self.ymax + 1)}
        field = ''
        for y in range(0, self.ymax + 1):
            field += f'{y:5} '
            for x in range(self.xmin - 2, self.xmax + 3):
                if y == 0 and x == 500: field += '+'
                elif (x, y) in self.settled: field += '~'
                elif (x, y) in self.reachable: field += '|'
                elif x in grid.get(y, ()): field += '#'
                else: field += '.'
            field += '\n'
        print(field)
        time.sleep(0.5)

    def is_sand(self, coord):
        return coord not in self.clay and coord not in self.settled

    def settle_bucket(self, y: int, coord_clay_left: Tuple[int, int], coord_clay_right: Tuple[int, int]):
        for x in range(right_from(coord_clay_left)[0], coord_clay_right[0]):
            self.settled.add((x, y))

    def search_left(self, coord: Tuple[int, int], next_sources) -> Tuple[bool, Tuple[int, int]]:
        """Return True if clay is found or False if we can go down, and the last examined coordinate."""
        next_coord = coord
        while True:
            next_coord = left_from(next_coord)
            if next_coord in self.clay:
                return True, next_coord
            self.reachable.add(next_coord)
            if self.is_sand(down_from(next_coord)):
                next_sources.append(next_coord)
                return False, next_coord

    def search_right(self, coord: Tuple[int, int], next_sources) -> Tuple[bool, Tuple[int, int]]:
        """Return True if clay is found or False if we can go down, and the last examined coordinate."""
        next_coord = coord
        while True:
            next_coord = right_from(next_coord)
            if next_coord in self.clay:
                return True, next_coord
            self.reachable.add(next_coord)
            if self.is_sand(down_from(next_coord)):
                next_sources.append(next_coord)
                return False, next_coord

    def find_water(self, debug=False):
        """Simply move down 1 block all the time. Could probably go a lot faster if grid/slice data
        would be structured such that range-lookups can be done."""
        backtrack_water_source = False
        previous_sources = []
        water_sources = [(500, 0)]
        next_sources = []
        while water_sources:
            for source in water_sources:
                breadcrumb = source

                while True:
                    # if debug: self.debug_grid()
                    below = down_from(breadcrumb)

                    if below in self.clay or below in self.settled:
                        found_clay_left, coord_clay_left = self.search_left(breadcrumb, next_sources)
                        found_clay_right, coord_clay_right = self.search_right(breadcrumb, next_sources)

                        if found_clay_left and found_clay_right:
                            if breadcrumb == source:
                                backtrack_water_source = True
                                break
                            self.settle_bucket(breadcrumb[1], coord_clay_left, coord_clay_right)
                            breadcrumb = up_from(breadcrumb)
                        else:
                            break  # new source on left or right
                    elif below[1] > self.ymax:
                        break  # out of bounds
                    else:
                        self.reachable.add(below)
                        breadcrumb = below

            if backtrack_water_source:
                next_sources = previous_sources.pop(len(previous_sources) - 1)
                backtrack_water_source = False
            else:
                previous_sources.append(water_sources)
            water_sources = next_sources
            next_sources = []

        water_total = len(self.settled.union(self.reachable)) - (self.ymin - 1)
        water_settled = len(self.settled)
        return water_total, water_settled


def parse_slices(unparsed):
    def line_to_tuples(rgx_group):
        if '..' in rgx_group[1]:
            return tuple(map(int, rgx_group[1].split('..')))
        return int(rgx_group[1]), int(rgx_group[1])

    def tuples_to_dict(slice_tuples):
        return dict((i[0], list(range(i[1][0], i[1][1] + 1))) for i in slice_tuples)

    slice_lines = [i.strip() for i in unparsed.splitlines() if i.strip()]
    converted = [[(i[0], line_to_tuples(i)) for i in re.findall(r'([xy])=([\d\.]+)', line)] for line in slice_lines]
    return sorted((tuples_to_dict(slice_list) for slice_list in converted), key=lambda item: item['x'][0])


def solve():
    north_pole = NorthPole(parse_slices(open('input.txt').read()))
    water_total, water_settled = north_pole.find_water()
    t_total = (time.time() - t_start) * 1000
    print('The answer to part 1 is ', water_total)
    print('The answer to part 2 is ', water_settled)
    print(f'Took {t_total:.2f}ms')


def test():
    example = ("x=495, y=2..7\ny=7, x=495..501\nx=501, y=3..7\nx=498, y=2..4\nx=506, y=1..2\nx=498, y=10..13\n"
               "x=504, y=10..13\ny=13, x=498..504\n")
    north_pole = NorthPole(parse_slices(example))
    water_total, water_settled = north_pole.find_water(debug=True)
    t_total = (time.time() - t_start) * 1000
    print('The answer to part 1 is ', water_total)
    print('The answer to part 2 is ', water_settled)
    print(f'Took {t_total:.2f}ms')


if __name__ == '__main__':
    # test()
    solve()
