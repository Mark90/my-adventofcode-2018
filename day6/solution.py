import string
from collections import defaultdict
from itertools import product
from math import ceil
from typing import Dict, Tuple, List


def calc_areas(coordinates: Dict[Tuple, str], width: int, height: int, border_offset: Tuple[int, int]):
    """For each location in the field, calculate the Manhattan Distance to each coordinate.
    If 1 coordinate is closest of all, increment its area.
    Return a dictionary of coordinate labels and their total area."""
    coordinate_areas = defaultdict(int)
    for y in range(width):
        for x in range(height):
            closest, tied = None, False
            for real_coord, label in coordinates.items():
                # Add border_offset to the coord while calculating the distance
                fictive_coord = real_coord[0] + border_offset[0], real_coord[1] + border_offset[1]

                if fictive_coord == (x, y):
                    # The coordinate's own location - we can stop looking
                    closest, tied = (label, 0), False
                    break

                manhattan_distance = abs(x - fictive_coord[0]) + abs(y - fictive_coord[1])
                try:
                    if manhattan_distance < closest[1]:
                        closest, tied = (label, manhattan_distance), False
                    elif manhattan_distance == closest[1]:
                        tied = True
                except TypeError:  # closest not yet set
                    closest, tied = (label, manhattan_distance), False

            if not tied:
                coordinate_areas[closest[0]] += 1
    return coordinate_areas


def run(labeled_coordinates: Dict[Tuple, str], border_width=0) -> Dict[str, int]:
    """Given the coordinates, determine size of the field and return calculated areas."""
    border_offset = (border_width, border_width)
    field_width = max(labeled_coordinates, key=lambda c: c[0])[0] + 1 + (2 * border_width)
    field_height = max(labeled_coordinates, key=lambda c: c[1])[1] + 1 + (2 * border_width)
    return calc_areas(labeled_coordinates, field_width, field_height, border_offset)


def add_labels(coordinates: List[Tuple]) -> Dict[Tuple, str]:
    """Returns dictionary of coordinates with unique ASCII labels."""
    label_chars = [char for char in string.ascii_uppercase]
    label_len = ceil(len(coordinates) / len(label_chars))
    labels = (''.join(item) for item in product(label_chars, repeat=label_len))
    return dict(zip(coordinates, labels))


def test():
    coordinates = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    labeled_coordinates = add_labels(coordinates)

    # Calculate areas twice - the second time with an extra 'border' around the field
    # This allows us to filter non-infinite areas and find the largest finite area
    areas = run(labeled_coordinates)
    areas_with_border = run(labeled_coordinates, border_width=1)
    finite_areas = {coord: size for coord, size in areas.items() if areas_with_border[coord] == size}
    largest_finite_area = max(finite_areas.items(), key=lambda x: x[1])

    print(f'[test] The largest non-infinite area: {largest_finite_area}')
    assert largest_finite_area == ('E', 17)


def solve():
    with open('input.txt') as f:
        coordinates = [tuple(map(int, i.strip().split(', '))) for i in f.readlines()]
    labeled_coordinates = add_labels(coordinates)

    # Calculate areas twice - the second time with an extra 'border' around the field
    # This allows us to filter non-infinite areas and find the largest finite area
    areas = run(labeled_coordinates)
    areas_with_border = run(labeled_coordinates, border_width=1)
    finite_areas = {coord: size for coord, size in areas.items() if areas_with_border[coord] == size}
    largest_finite_area = max(finite_areas.items(), key=lambda x: x[1])

    print(f'The largest non-infinite area: {largest_finite_area}')


if __name__ == '__main__':
    test()
    solve()
