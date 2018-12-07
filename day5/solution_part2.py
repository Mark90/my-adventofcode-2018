import string


def react(composition_string: str, filter_unit: str) -> str:
    """React the polymer composition until there
    are no adjacent characters of opposing polarity."""
    opposite_polarity = {k: k.upper() for k in string.ascii_lowercase}
    opposite_polarity.update({k: k.lower() for k in string.ascii_uppercase})

    composition = [i for i in composition_string if i.lower() != filter_unit]
    position = 1
    try:
        while True:
            if composition[position - 1] == opposite_polarity[composition[position]]:
                del composition[position - 1:position + 1]
                position = max(1, position - 1)
            else:
                position += 1
    except IndexError:
        return ''.join(composition)


def fully_react(composition: str) -> str:
    """Find the most compact composition while removing a unit before the reaction.
    Repeat for every type of unit."""
    compositions = {filter_unit: react(composition, filter_unit) for filter_unit in string.ascii_lowercase}
    return min(compositions.values(), key=lambda x: len(x))


def test():
    composition = 'dabAcCaCBAcCcaDA'
    result = fully_react(composition)
    print(f'[test] Number of units in the resulting polymer: {len(result)}')
    assert len(result) == 4
    assert result == 'daDA'


def solve():
    with open('input.txt') as f:
        composition = f.read().strip()
    result = fully_react(composition)
    print(f'Number of units in the resulting polymer: {len(result)}')


if __name__ == '__main__':
    test()
    solve()
