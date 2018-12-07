import string


def react(composition_string: str) -> str:
    """React the polymer composition until there
    are no adjacent characters of opposing polarity."""
    opposite_polarity = {k: k.upper() for k in string.ascii_lowercase}
    opposite_polarity.update({k: k.lower() for k in string.ascii_uppercase})

    composition = [i for i in composition_string]
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


def test():
    composition = 'dabAcCaCBAcCcaDA'
    result = react(composition)
    print(f'[test] Number of units in the resulting polymer: {len(result)}')
    assert len(result) == 10
    assert result == 'dabCBAcaDA'


def solve():
    with open('input.txt') as f:
        composition = f.read().strip()
    result = react(composition)
    print(f'Number of units in the resulting polymer: {len(result)}')


if __name__ == '__main__':
    test()
    solve()
