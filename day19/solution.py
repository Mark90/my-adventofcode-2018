"""Reverse engineering opcode instructions. Fun fun fun..

Part 1: ~7s      (<20ms reverse engineered)
Part 2: ~2200ms  (obviously reverse engineered)

Python 3.7, Intel i5 7200u
"""
import time

from day16.solution import opcodes as opcode_funcs

opcodes = {f.__name__: f for f in opcode_funcs}


def run_program(registers, instructions, ip, stop_after_init=False):
    ip_value = 0
    executed = 0
    while True:
        try:
            current_instruction = instructions[ip_value]
        except KeyError:
            return executed
        registers[ip] = ip_value
        func_name, *args = current_instruction
        if stop_after_init and func_name == 'mulr' and args == [5, 3, 1]:
            return executed
        opcodes[func_name](registers, *args)
        ip_value = registers[ip]
        ip_value += 1
        executed += 1


def test():
    text = "#ip 0\nseti 5 0 1\nseti 6 0 2\naddi 0 1 0\naddr 1 2 3\nsetr 1 0 0\nseti 8 0 4\nseti 9 0 5"
    ip_line, *instruction_lines = [l.strip() for l in text.splitlines() if l.strip()]
    ip = int(ip_line.replace('#ip ', ''))
    instructions = {idx: (i.split(' ')[0], *map(int, i.split(' ')[1:])) for idx, i in enumerate(instruction_lines)}
    registers = [0, 0, 0, 0, 0, 0]
    print('Test: registers before:', registers)
    executed = run_program(registers, instructions, ip)
    print(f'Test: registers after {executed} instructions:', registers)
    print('Test: register 0:', registers[0], '\n')


def calculate_final_value(registers):
    registers[0] = sum(i for i in range(1, registers[2] + 1) if (registers[2] % i) == 0)


def part1(skip=False):
    t_start = time.time()
    text = open('input.txt').read()
    ip_line, *instruction_lines = [l.strip() for l in text.splitlines() if l.strip()]
    ip = int(ip_line.replace('#ip ', ''))
    instructions = {idx: (i.split(' ')[0], *map(int, i.split(' ')[1:])) for idx, i in enumerate(instruction_lines)}
    registers = [0, 0, 0, 0, 0, 0]
    print('Part 1: registers before:', registers)
    executed = run_program(registers, instructions, ip, stop_after_init=skip)
    print(f'Part 1: registers after {executed} instructions:', registers)
    if skip:
        calculate_final_value(registers)
        print('Part 1: calculated final position of register 0')
    print('Part 1: register 0:', registers[0], f'(took {(time.time() - t_start) * 1000:.2f}ms\n')


def part2():
    t_start = time.time()
    text = open('input.txt').read()
    ip_line, *instruction_lines = [l.strip() for l in text.splitlines() if l.strip()]
    ip = int(ip_line.replace('#ip ', ''))
    instructions = {idx: (i.split(' ')[0], *map(int, i.split(' ')[1:])) for idx, i in enumerate(instruction_lines)}
    registers = [1, 0, 0, 0, 0, 0]
    print('Part 2: registers before:', registers)
    executed = run_program(registers, instructions, ip, stop_after_init=True)
    print(f'Part 2: registers after {executed} instructions:', registers)
    calculate_final_value(registers)
    print('Part 2: calculated final position of register 0')
    print('Part 2: register 0:', registers[0], f'(took {(time.time() - t_start) * 1000:.2f}ms\n')


if __name__ == '__main__':
    test()
    part1()
    part1(skip=True)
    part2()
