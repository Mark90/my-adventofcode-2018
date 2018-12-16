"""Bitwise operations! Yay!
Been a while I really used them - I was often mixing up the index of a bit and its power of 2.
Hence the helper functions with doctests to visualize the problem.
Took ~2h30m to solve it, easy pace.

Excution: ~60ms on an Intel i7 870
"""
import time

char_to_bit = {
    '#': '1',
    '.': '0',
}
bit_to_char = {
    '1': '#',
    '0': '.',
}


def str_to_int(string: str) -> int:
    """
    Doctest:
        >>> bin(str_to_int('##.##'))
        '0b11011'
        >>> bin(str_to_int('.....'))
        '0b0'
        >>> bin(str_to_int('#....'))
        '0b10000'
        >>> bin(str_to_int('##'))
        '0b11'
    """
    return int(''.join(char_to_bit[c] for c in string), 2)


def int_to_str(number: int) -> str:
    """
    Doctest:
        >>> int_to_str(0b00000)
        '.'
        >>> int_to_str(0b10000)
        '#....'
        >>> int_to_str(0b10010)
        '#..#.'
        >>> int_to_str(0b11111)
        '#####'
    """
    return ''.join(bit_to_char[c] for c in bin(number)[2:])


def lowest_enabled_bit(number: int) -> int:
    """
    Doctest:
        >>> lowest_enabled_bit(0b000000)
        >>> lowest_enabled_bit(0b000001) # 2**0
        1
        >>> lowest_enabled_bit(0b000010) # 2**1
        2
        >>> lowest_enabled_bit(0b000100) # 2**2
        3
        >>> lowest_enabled_bit(0b001010) # 2**3 + 2**1
        2
    """
    binary = bin(number)[2:]
    return len(binary) - binary.rfind('1') if '1' in binary else None


def num_bits(number: int) -> int:
    """
    Doctest:
        >>> num_bits(0b0)
        1
        >>> num_bits(0b1)
        1
        >>> num_bits(0b100)
        3
        >>> num_bits(0b111)
        3
    """
    return len(bin(number)[2:])


def sum_of_pots_with_plants(number: int, base_idx: int) -> int:
    """Translate state number to state string.
    Base_idx tells us the pot-id of the left-most pot with a plant.
    This allows us to enumerate pots with the correct id.
    Then we sum the indices of all pots containing plants.

    Doctest:
        >>> sum_of_pots_with_plants(0b1000, 0)
        0
        >>> sum_of_pots_with_plants(0b1111, 0)
        6
        >>> sum_of_pots_with_plants(0b1000, 2)
        2
        >>> sum_of_pots_with_plants(0b1000, -2)
        -2
        >>> sum_of_pots_with_plants(0b1111, 2)
        14
    """
    return sum(idx for idx, value in enumerate(int_to_str(number), base_idx) if value == '#')


def leftpad(number: int, width=50):
    """Visualize current state"""
    string = int_to_str(number)
    return '.' * max(0, width - len(string)) + string


# Part2 config
start_string_part2 = '##.#..#.#..#.####.#########.#...#.#.#......##.#.#...##.....#...#...#.##.#...##...#.####.##..#.#..#.'
num_generations_part2 = 50000000000
combinations_part2 = [str_to_int(comb) for comb in [
    '.#.#.',
    '.#...',
    '#####',
    '#..#.',
    '#...#',
    '###.#',
    '...##',
    '#.##.',
    '.#.##',
    '##.#.',
    '..###',
    '###..',
    '##..#',
    '#..##',
]]

# Test config
start_string_test = '#..#.#..##......###...###'
num_generations_test = 20
combinations_test = [str_to_int(comb) for comb in [
    '...##',
    '..#..',
    '.#...',
    '.#.#.',
    '.#.##',
    '.##..',
    '.####',
    '#.#.#',
    '#.###',
    '##.#.',
    '##.##',
    '###..',
    '###.#',
    '####.',
]]

if __name__ == '__main__':
    t_start = time.time()

    start_string, combinations, num_generations = start_string_part2, combinations_part2, num_generations_part2
    # start_string, combinations, num_generations = start_string_test, combinations_test, num_generations_test

    # Shift the number left enough to allow plants to spread "to the right"
    # We'll do this more often during the algorithm.
    # It doesn't matter how often we do this - pots are identified from the leftmost (highest) bit
    current_number = str_to_int(start_string) << 3

    # This variable is key in our algorithm.
    # When the highest bit shifts left, decrement base_idx as much.
    # When the highest bit shifts right, increment base_idx as much.
    base_idx = 0

    # Keep track of the change in sum
    current_sum = sum_of_pots_with_plants(current_number, base_idx)
    current_sumchange = 0

    # print(f'START: STATE=[{leftpad(current_number)}]  num_bits={num_bits(current_number)}')
    for generation in range(num_generations):
        if generation > 0:
            # Break if the sum changes at a constant rate
            new_sum = sum_of_pots_with_plants(current_number, base_idx)
            new_sumchange = new_sum - current_sum
            # print(f'GEN={generation:2d}  STATE=[{leftpad(current_number)}]  num_bits={num_bits(current_number)}  '
            #       f' SUM [{current_sum} -> {new_sum}] sumchange {new_sumchange})')
            if current_sumchange == new_sumchange:
                remaining_generations = num_generations - generation
                final_sum = int(new_sum + (remaining_generations * new_sumchange))
                time_needed = (time.time() - t_start) * 1000
                raise Exception(
                    f'Sum increases at constant rate. Calculated final value after {remaining_generations} more '
                    f'generations: {final_sum}. (Took {time_needed:.5f}ms)')
            current_sum = new_sum
            current_sumchange = new_sumchange

        # The 2 lowest bits should always be empty
        if lowest_enabled_bit(current_number) <= 3:
            current_number <<= 2

        current_bit_count = num_bits(current_number)
        next_number = 0  # By starting with an empty number, we don't need to check "plant prohibiting" combinations
        for current_bit in range(0, current_bit_count + 1):
            bits_to_compare = (current_number & (0b11111 << current_bit)) >> current_bit
            for comb in combinations:  # check if any combination allows a plant in the center pot of the masked bits
                if (comb ^ bits_to_compare) == 0:
                    next_number |= 2 ** (current_bit + 2)  # add the center pot to the next state
                    break

        current_number = next_number
        base_idx -= (num_bits(current_number) - current_bit_count)

    print(f'DONE:  STATE=[{leftpad(current_number)}]   num_bits={num_bits(current_number)}')
    print('Final SUM (test should be 325):', sum_of_pots_with_plants(current_number, base_idx))
