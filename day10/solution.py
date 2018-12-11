"""This one took quite long to figure out, about 3 hours.
The x/y scaling isn't needed, but it's how I finally saw the solution.
A fun exercise."""
import re
import time

lines = [i.strip() for i in open('input.txt') if i.strip()]
rgx = r'position=<\s*([-]{0,1}\d+),\s*([-]{0,1}\d+)> velocity=<\s*([-]{0,1}\d+),\s*([-]{0,1}\d+)>'
lights = [tuple(map(int, re.match(rgx, line).groups())) for line in lines]

target_width = 100.0
target_height = 0.15 * target_width

sleep = 0.01

t = time.time()

time_passed = 0
while True:
    realxmin = min(lights, key=lambda x: x[0])[0]
    realxmax = max(lights, key=lambda x: x[0])[0] + 1
    realymin = min(lights, key=lambda x: x[1])[1]
    realymax = max(lights, key=lambda x: x[1])[1] + 1

    scale_x = target_width / float(realxmax - realxmin)
    scale_y = target_height / float(realymax - realymin)

    if realxmax > 40000:
        speedup = 3000
    elif realxmax > 10000:
        speedup = 800
    elif realxmax > 1000:
        speedup = 20
    elif realxmax > 500:
        speedup = 5
    else:
        speedup = 1

    print(f't={time.time() - t:.2f} scale_x={scale_x:.5f} scale_y={scale_y:.5f} speedup={speedup} sleep={sleep}  '
          f'x=[{realxmin}, {realxmax}] y=[{realymin}, {realymax}]')

    if (realxmin, realxmax) == (117, 179):
        # draw lights with scaled coordinates
        draw = {(int(scale_x * i[0]), int(scale_y * i[1])): '#' for i in lights}

        xmin = min(draw, key=lambda x: x[0])[0]
        xmax = max(draw, key=lambda x: x[0])[0] + 1
        ymin = min(draw, key=lambda x: x[1])[1]
        ymax = max(draw, key=lambda x: x[1])[1] + 1
        solution = ''
        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                solution += draw.get((x, y), '.')
            solution += '\n'
        # solution @ t=40.23 scale_x=2.01613 scale_y=1.87500 speedup=1 sleep=0.25  x=[117, 179] y=[156, 166]
        print(f'\nSOLUTION\n\n{solution}')
        print(f'Time passed: {time_passed}')
        break

    # update
    lights = [(i[0] + (speedup * i[2]), i[1] + (speedup * i[3]), i[2], i[3]) for i in lights]
    time_passed += speedup
    time.sleep(sleep)
