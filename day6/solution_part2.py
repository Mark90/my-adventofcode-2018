import string
from itertools import product
from math import ceil
from typing import Dict, Tuple, List


def find_region_with_distance_to_coords(coordinates: Dict[Tuple, str], width: int, height: int, threshold: int):
    """Count how many locations in the field have a total distance to all coordinates less than `threshold`."""
    region_size = 0
    for y in range(width):
        for x in range(height):
            distance_to_coords = 0
            for coord in coordinates:
                distance_to_coords += abs(x - coord[0]) + abs(y - coord[1])

            if distance_to_coords < threshold:
                region_size += 1
    return region_size


def add_labels(coordinates: List[Tuple]) -> Dict[Tuple, str]:
    """Returns dictionary of coordinates with unique ASCII labels."""
    label_chars = [char for char in string.ascii_uppercase]
    label_len = ceil(len(coordinates) / len(label_chars))
    labels = (''.join(item) for item in product(label_chars, repeat=label_len))
    return dict(zip(coordinates, labels))


def test():
    coordinates = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    distance_threshold = 32
    labeled_coordinates = add_labels(coordinates)

    field_width = max(labeled_coordinates, key=lambda c: c[0])[0] + 1
    field_height = max(labeled_coordinates, key=lambda c: c[1])[1] + 1
    region = find_region_with_distance_to_coords(labeled_coordinates, field_width, field_height, distance_threshold)

    print(f'[test] The size of the region is: {region}')
    assert region == 16


def solve():
    with open('input.txt') as f:
        coordinates = [tuple(map(int, i.strip().split(', '))) for i in f.readlines()]
    distance_threshold = 10000
    labeled_coordinates = add_labels(coordinates)

    field_width = max(labeled_coordinates, key=lambda c: c[0])[0] + 1
    field_height = max(labeled_coordinates, key=lambda c: c[1])[1] + 1
    region = find_region_with_distance_to_coords(labeled_coordinates, field_width, field_height, distance_threshold)

    print(f'The size of the region is: {region}')


if __name__ == '__main__':
    test()
    solve()
