"""Updated for part 2.

Using a doubly linked list as python's list insert is O(N)
Much faster this way, but memory usage peaks at almost 1200MB
I have no doubt there's a fancy math solution to overcome this. :-)
"""
import re


class Marble:
    value: int
    left: 'Marble' = None
    right: 'Marble' = None

    def __init__(self, value):
        self.value = value

    def insert_right(self, marble: 'Marble') -> 'Marble':
        """Insert marble to the right of this one and return it"""
        marble.right = self.right
        self.right.left = marble
        self.right = marble
        marble.left = self
        return marble

    def pop(self) -> 'Marble':
        """Pop this marble from the chain and return the one taking its place"""
        self.left.right, self.right.left = self.right, self.left  # ol' switcharoo
        return self.right

    def get_7_left(self) -> 'Marble':
        return self.left.left.left.left.left.left.left  # Hm?


def play_until(num_players, last_marble):
    scores = {i: 0 for i in range(num_players)}

    root = Marble(value=0)
    root.left = root.right = root
    current_player = 0
    for marble_value in range(1, last_marble + 1):
        current_player = (current_player + 1) % num_players

        if (marble_value % 23) == 0:
            marble_to_take = root.get_7_left()
            root = marble_to_take.pop()
            scores[current_player] += marble_value + marble_to_take.value
        else:
            root = root.right.insert_right(Marble(value=marble_value))
    return max(scores.values())


def test():
    lines = """9 players; last marble is worth 25 points: high score is 32
    10 players; last marble is worth 1618 points: high score is 8317
    13 players; last marble is worth 7999 points: high score is 146373
    17 players; last marble is worth 1104 points: high score is 2764
    21 players; last marble is worth 6111 points: high score is 54718
    30 players; last marble is worth 5807 points: high score is 37305"""

    for line in lines.splitlines():
        example = re.match(r'(\d+) play.+rth (\d+) po.+is (\d+)', line.strip()).groups()
        players, last_marble, expected_score = map(int, example)
        actual_score = play_until(players, last_marble)
        print(f'[test] Score with {players} players and {last_marble} marbles: {actual_score}')
        assert actual_score == expected_score


def solve():
    with open('input.txt') as f:
        question = re.match(r'(\d+) play.+rth (\d+).+', f.read().strip()).groups()
    players, last_marble = map(int, question)
    actual_score = play_until(players, last_marble)
    print(f'[part1] Score with {players} players and {last_marble} marbles: {actual_score}')


def solve_part2():
    with open('input.txt') as f:
        question = re.match(r'(\d+) play.+rth (\d+).+', f.read().strip()).groups()
    players, last_marble = map(int, question)
    last_marble *= 100
    actual_score = play_until(players, last_marble)
    print(f'[part2] Score with {players} players and {last_marble} marbles: {actual_score}')


if __name__ == '__main__':
    test()
    solve()
    solve_part2()
