"""
~1100ms, Python 3.7, Intel i5-7200U
"""

import time

t_start = time.time()

e1 = 0
e2 = 1

allreci = [3, 7]

inp = 864801

created = 2
for i in range(inp + 10):
    r1, r2 = allreci[e1], allreci[e2]

    nr = r1 + r2
    nr1, nr2 = nr // 10, nr % 10

    if nr1 ^ 0:
        allreci.append(nr1)
        created += 1
    allreci.append(nr2)
    created += 1

    e1 = (e1 + 1 + r1) % created
    e2 = (e2 + 1 + r2) % created

    if created >= (inp + 10):
        break

t = (time.time() - t_start) * 1000
print(f'Completed in {t:.2f}ms\n'
      f'Created {created} recipes\n'
      f'Next 10 after the first {inp}: {"".join(str(c) for c in allreci[inp:inp + 10])}')
