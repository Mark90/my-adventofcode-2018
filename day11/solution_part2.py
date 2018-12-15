"""Couldn't solve it.

Spent 6 hours trying to make it performant, calculating sum of a grid based on smaller
previously calculated grids, etc. Eventually looked at reddit and learned about Summed-area tables.
No more energy to work it out on my own, I copied the C++ solution by 'tribulu'
https://www.reddit.com/r/adventofcode/comments/a53r6i/2018_day_11_solutions/ebjogd7
"""
from collections import defaultdict

sums = defaultdict(lambda: defaultdict(int))
gridsize = 1955

for y in range(1, 301):
    for x in range(1, 301):
        p = ((((((x + 10) * y) + gridsize) * (x + 10)) // 100) % 10) - 5
        sums[y][x] = p + sums[y - 1][x] + sums[y][x - 1] - sums[y - 1][x - 1]

bx = by = bs = best = 0

for s in range(1, 301):
    print(s)
    for y in range(1, 301):
        for x in range(1, 301):
            total = sums[y][x] - sums[y - s][x] - sums[y][x - s] + sums[y - s][x - s]
            if total > best:
                best = total
                bx = x
                by = y
                bs = s

print(f'{bx - bs + 1},{by - bs + 1},{bs}')
