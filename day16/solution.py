"""~250ms, Python 3.7, Intel i7 870"""
import time
from collections import defaultdict


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


def part1():
    t_start = time.time()

    with open('input.txt') as f:
        data = f.read()
        samples = data.split('\n\n\n')[0].split('\n\n')

    opcode_similarity_counts = defaultdict(int)
    for sample in samples:
        sample = [line.strip() for line in sample.splitlines()]
        str_registry_before, instruction, str_registry_after = sample
        _, a, b, c = map(int, instruction.split(' '))
        similar_opcodes = 0
        registry_after = eval(str_registry_after.split(': ')[1])
        registry_before = str_registry_before.split(': ')[1]
        for func in opcodes:
            reg_in = eval(registry_before)
            func(reg_in, a, b, c)
            if reg_in == registry_after:
                similar_opcodes += 1
        opcode_similarity_counts[similar_opcodes] += 1
    answer_part1 = sum(count for similar_opcodes, count in opcode_similarity_counts.items() if similar_opcodes >= 3)
    t_done = (time.time() - t_start) * 1000
    print(answer_part1, f'Found in {t_done:.2f}ms')


if __name__ == '__main__':
    part1()
