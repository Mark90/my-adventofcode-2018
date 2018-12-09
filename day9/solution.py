import re


def index_to_put(circle, current_marble):
    """Decide index at which the next marble should be inserted.
    Marble at that index will be moved clockwise."""
    if len(circle) == 1:
        return 1
    return (current_marble + 2) % (len(circle))


def index_to_take(circle, current_marble):
    """Decide index from which a marble should be removed."""
    return (current_marble - 7) % len(circle)


def play_until(num_players, last_marble):
    scores = {i: 0 for i in range(num_players)}
    circle = [0]
    current_marble = current_player = 0
    for new_marble in range(1, last_marble + 1):
        current_player = (current_player + 1) % num_players

        if (new_marble % 23) == 0:
            take = index_to_take(circle, current_marble)
            scores[current_player] += new_marble + circle.pop(take)
            current_marble = take % len(circle)
        else:
            put = index_to_put(circle, current_marble)
            circle.insert(put, new_marble)
            current_marble = put
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
    print(f'Score with {players} players and {last_marble} marbles: {actual_score}')


if __name__ == '__main__':
    test()
    solve()
