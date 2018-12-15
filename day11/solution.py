from collections import defaultdict


def get_pl(gridserialnumber):
    pl = defaultdict(dict)
    for x in range(1, 301):
        for y in range(1, 301):
            rackid = x + 10
            p = rackid * y
            p += gridserialnumber
            p = p * rackid
            p = int(str(p)[-3]) if len(str(p)) >= 3 else 0
            p -= 5
            pl[x][y] = p
    return pl


powerlevels = get_pl(1955)
max_xy = 0, 0
max_pl = 0
for x in range(1, 301 - 3):
    for y in range(1, 301 - 3):
        l = sum(powerlevels[xx][yy] for xx in range(x, x + 3) for yy in range(y, y + 3))
        if l > max_pl:
            max_pl = l
            max_xy = x, y

print(max_pl)
print(max_xy)
