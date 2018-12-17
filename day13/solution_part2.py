"""~240 seconds"""
import time

t_start = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines() if line.strip()]

protected = {'>', '<', '^', 'v'}

curves = {'/', '\\'}

get_newdir = {
    'left': 'straight',
    'straight': 'right',
    'right': 'left',
}

default_path_cache = {  # initial character to put at path after cart leaves it - no carts start on a curved path
    '>': '-',
    'v': '|',
    '<': '-',
    '^': '|',
}


def get_newxy(x, y, cart):
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
grid = {y: {x: None for x in range(150)} for y in range(150)}
cart_locations = {}  # administer location and last picked direction for each cart
path_cache = {}  # remember the path for a location a cart is currently on
for y, line in enumerate(lines):
    for x, field in enumerate(line):
        grid[y][x] = field
        if field in protected:
            cart_locations[(x, y)] = 'left'
            path_cache[(x, y)] = default_path_cache[field]

print(f'Start with {len(cart_locations)} carts')

i = 0
while True:
    if len(cart_locations) == 1:
        time_in_ms = (time.time() - t_start) * 1000
        raise Exception(f'Last cart at: {cart_locations} (Found in {time_in_ms:.2f}ms)')

    new_grid = {y: {x: None for x in range(150)} for y in range(150)}

    carts_deleted = []
    for y, row in grid.items():
        for x, curfield in row.items():
            if curfield not in protected:
                if new_grid[y][x] is None:
                    new_grid[y][x] = curfield
                # else: we have already assigned a cart here
                continue

            if (x, y) in carts_deleted:
                # it's already deleted in new_grid
                continue

            # a cart! let's try to move it
            newxy = get_newxy(x, y, curfield)
            new_x, new_y = newxy
            if newxy in cart_locations:
                curxy = x, y
                # remove both carts and restore paths in new_grid
                del cart_locations[curxy], cart_locations[newxy]
                time_in_ms = (time.time() - t_start) * 1000
                print(f'{i} Collision at {newxy}! Remaining carts: {len(cart_locations)} (Found in {time_in_ms:.2f}ms)')
                carts_deleted.extend([curxy, newxy])
                new_grid[y][x] = path_cache[curxy]
                new_grid[new_y][new_x] = path_cache[newxy]
                del path_cache[curxy], path_cache[newxy]
                continue

            # get the next field
            nextfield = new_grid[new_y][new_x] or grid[new_y][new_x]
            if nextfield == '+':  # if intersection: pick a direction
                curdir = cart_locations[x, y]
                # Set new next intersect direction
                cart_locations[x, y] = get_newdir[curdir]
                # and adjust field accordingly
                newfield = get_direction_newfield[curfield].get(curdir, curfield)  # 'straight' -> no change
            elif nextfield in curves:  # if curved: adjust symbol accordingly
                newfield = get_curve_newfield[curfield][nextfield]
            else:  # follow the same path
                newfield = curfield

            # restore current field from path_cache
            new_grid[y][x] = path_cache[x, y]

            # cache the path for next location
            path_cache[newxy] = nextfield

            # move item in cart_locations and new_grid
            cart_locations[newxy] = cart_locations.pop((x, y))
            new_grid[new_y][new_x] = newfield

    # make newgrid the new grid.
    grid = new_grid
    i += 1
