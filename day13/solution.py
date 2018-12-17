"""~2.3sec"""
import time
from collections import defaultdict

t_start = time.time()

with open('input.txt') as f:
    lines = [line for line in f.readlines() if line.strip()]

protected = {'>', '<', '^', 'v'}


def get_newdir(d):
    if d == 'left':
        return 'straight'
    if d == 'straight':
        return 'right'
    return 'left'


default_path_cache = {  # initial character to put at path after cart leaves it - no carts start on a curved path
    '>': '-',
    'v': '|',
    '<': '-',
    '^': '|',
}


def get_newxy(xy, cart):
    x, y = xy
    if cart == '<':
        return x - 1, y
    if cart == '>':
        return x + 1, y
    if cart == 'v':
        return x, y + 1
    if cart == '^':
        return x, y - 1


get_direction_newfield = {
    '>': {'left': '^', 'right': 'v'},
    '<': {'left': 'v', 'right': '^'},
    'v': {'left': '>', 'right': '<'},
    '^': {'left': '<', 'right': '>'},
}

get_curve_newfield = {
    '>': {'\\': 'v', '/': '^'},
    '<': {'\\': '^', '/': 'v'},
    'v': {'\\': '>', '/': '<'},
    '^': {'\\': '<', '/': '>'},
}

# Populate grid, cart locations, path cache
grid = {}
cart_locations = {}  # administer location and last picked direction for each cart
path_cache = {}  # remember the path for a location a cart is currently on
for y, line in enumerate(lines):
    for x, field in enumerate(line):
        grid[(x, y)] = field
        if field in protected:
            cart_locations[(x, y)] = 'left'
            path_cache[(x, y)] = default_path_cache[field]


def render(grid):
    tmp = defaultdict(dict)
    for el in sorted(grid, key=lambda field: (field[1], field[0])):
        tmp[el[1]][el[0]] = grid[el]
    s = ''
    for y, row in tmp.items():
        for x, field in row.items():
            s += field
        s += '\n'
    print(s)


sleep = 0

i = 0
while True:
    if (i % 1000) == 0:
        print(i)

    # render(grid)
    new_grid = {}
    for curxy, curfield in grid.items():
        if curfield not in protected:
            if curxy not in new_grid:
                new_grid[curxy] = curfield
            # else: we have already assigned a cart here
            continue

        # a cart! let's try to move it
        newxy = get_newxy(curxy, curfield)
        if newxy in cart_locations:
            time_in_ms = (time.time() - t_start) * 1000
            raise Exception(f'Collision at {newxy}! (Found in {time_in_ms:.2f}ms)')

        # get the next field
        nextfield = grid[newxy]

        if nextfield == '+':  # if intersection: pick a direction
            curdir = cart_locations[curxy]
            # Set new next intersect direction
            cart_locations[curxy] = get_newdir(curdir)
            # and adjust field accordingly
            newfield = get_direction_newfield[curfield].get(curdir, curfield)  # 'straight' -> no change
        elif nextfield in {'/', '\\'}:  # if curved: adjust symbol accordingly
            newfield = get_curve_newfield[curfield][nextfield]
        else:  # follow the same path
            newfield = curfield

        # restore current field from path_cache
        new_grid[curxy] = path_cache[curxy]

        # cache the path for next location
        path_cache[newxy] = nextfield

        # always: move item in cart_locations and new_grid
        cart_locations[newxy] = cart_locations.pop(curxy)
        new_grid[newxy] = newfield

    # make newgrid the new grid.
    grid = new_grid
    i += 1
