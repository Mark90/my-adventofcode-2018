"""~270ms, Python 3.7, Intel i7 870"""

import time
from collections import defaultdict
from functools import reduce


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]


def addi(reg, a, b, c):
    reg[c] = reg[a] + b


def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]


def muli(reg, a, b, c):
    reg[c] = reg[a] * b


def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]


def bani(reg, a, b, c):
    reg[c] = reg[a] & b


def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]


def bori(reg, a, b, c):
    reg[c] = reg[a] | b


def setr(reg, a, b, c):
    reg[c] = reg[a]


def seti(reg, a, b, c):
    reg[c] = a


def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0


def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0


def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0


def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0


def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0


def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0


opcodes = [addr,
           addi,
           mulr,
           muli,
           banr,
           bani,
           borr,
           bori,
           setr,
           seti,
           gtir,
           gtri,
           gtrr,
           eqir,
           eqri,
           eqrr]


def map_numbers_to_opcode(samples):
    number_to_opcode_sets = defaultdict(list)
    for sample in samples:
        sample = [line.strip() for line in sample.splitlines()]
        str_registry_before, instruction, str_registry_after = sample
        number, a, b, c = map(int, instruction.split(' '))

        registry_after = eval(str_registry_after.split(': ')[1])
        registry_before = str_registry_before.split(': ')[1]

        opcodes_matching_sample = set()
        for func in opcodes:
            reg_in = eval(registry_before)
            func(reg_in, a, b, c)
            if reg_in == registry_after:
                opcodes_matching_sample.add(func.__name__)

        if opcodes_matching_sample:
            number_to_opcode_sets[number].append(opcodes_matching_sample)

    number_to_opcodes = {}
    for n, opcode_sets in number_to_opcode_sets.items():
        number_to_opcodes[n] = reduce(lambda x, y: x.intersection(y), opcode_sets)

    result = {}
    while len(result) < len(number_to_opcode_sets):
        numbers_resolved = {k: v.pop() for k, v in number_to_opcodes.items() if len(v) == 1}
        result.update(numbers_resolved)
        number_to_opcodes = {k: [i for i in v if i not in numbers_resolved.values()]
                             for k, v in number_to_opcodes.items()}
    return result


def part2():
    t_start = time.time()
    with open('input.txt') as f:
        data = f.read().split('\n\n\n')
    samples = data[0].split('\n\n')
    instructions = [map(int, i.split(' ')) for i in data[1].splitlines() if i.strip()]

    number_to_opcode = {k: eval(v) for k, v in map_numbers_to_opcode(samples).items()}
    register = [0, 0, 0, 0]
    for number, a, b, c in instructions:
        number_to_opcode[number](register, a, b, c)

    answer_part2 = register[0]
    t_done = (time.time() - t_start) * 1000
    print(answer_part2, f'Found in {t_done:.2f}ms')


if __name__ == '__main__':
    part2()
