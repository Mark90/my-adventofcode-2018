"""
~3800ms, Python 3.7, intel i5 7200u
Min dps is not hardcoded
"""
import math
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Dict

t_start = time.time()


@dataclass(repr=False)
class Creature:
    health: int = 200
    dps: int = 3
    last_moved: int = None
    elf_dps: int = None

    def __repr__(self):
        return f'<{self.__class__.__name__} HP {self.health} lastmoved {self.last_moved}>'

    def is_enemy_of(self, other: 'Creature') -> bool:
        return type(self) != type(other)

    def attack(self, other: 'Creature'):
        other.health -= self.dps

    def dead(self) -> bool:
        return self.health < 1


class Goblin(Creature):
    """Scum of middle earth"""


@dataclass(repr=False)
class Elf(Creature):
    """Santa's tweaked little helpers"""

    def __post_init__(self):
        self.dps = self.elf_dps


class AnElfHasDied(Exception):
    """Skip this battle because an Elf already died"""


@dataclass(order=False, repr=False)
class Node:
    pos: Tuple[int, int]
    nodes: Dict[Tuple[int, int], 'Node']
    neighbors: List['Node'] = field(default_factory=list)
    creature: Creature = None

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.pos}>'

    def evaluate(self, rounds) -> int:
        """Return number of actions taken"""
        if not self.creature or self.creature.last_moved == rounds:
            return 0

        shortest_path = self.shortest_path_to_enemy()
        if shortest_path is None:
            return 0

        next_node, distance, final_node = shortest_path
        acting_node = self
        actions = 0
        if distance >= 1:
            self.creature.last_moved = rounds
            next_node.creature = self.creature
            self.creature = None
            distance -= 1
            acting_node = next_node
            actions += 1

        if distance == 0:
            lowest_hp = sorted([n for n in acting_node.neighbors if acting_node.contains_enemy(n)],
                               key=lambda i: (i.creature.health, i))[0]
            acting_node.creature.attack(lowest_hp.creature)
            actions += 1
            if lowest_hp.creature.dead():
                if isinstance(lowest_hp.creature, Elf):
                    raise AnElfHasDied()
                lowest_hp.creature = None
        return actions

    def contains_enemy(self, other_node: 'Node') -> bool:
        return other_node.creature is not None and other_node.creature.is_enemy_of(self.creature)

    def contains_ally(self, other_node: 'Node') -> bool:
        return other_node.creature is not None and not other_node.creature.is_enemy_of(self.creature)

    def shortest_path_to_enemy(self) -> Union[None, Tuple['Node', int, 'Node']]:
        """Some kind of breadth-first search mutation
        Nodeset for next iteration is created as we go
        The unvisited list and node.pos/self.nodes stuff is a mess, but can't be bothered
        for aesthetics after 8 hours of looking at this"""
        visited = set()
        unvisited = [(node.pos, 0, node.pos) for node in self.neighbors]
        distances = {node.pos: {} for node in self.neighbors}
        while unvisited:
            enemies_found = False
            next_unvisited = []
            for base_neighbor, steps, other_node in unvisited:
                if self.contains_ally(self.nodes[other_node]):
                    continue
                visited.add(other_node)
                if other_node in distances[base_neighbor]:
                    continue
                distances[base_neighbor][other_node] = steps
                enemies_found |= self.contains_enemy(self.nodes[other_node])
                if not enemies_found:
                    next_unvisited.extend([base_neighbor, distances[base_neighbor][other_node] + 1, new_node.pos]
                                          for new_node in self.nodes[other_node].neighbors
                                          if new_node.pos not in visited)

            if enemies_found:
                return sorted([
                    (self.nodes[next_node], distances[next_node][final_node], self.nodes[final_node])
                    for next_node, _, final_node in unvisited if self.contains_enemy(self.nodes[final_node])
                ], key=lambda choice: (choice[1], choice[2], choice[0]))[0]
            unvisited = next_unvisited

    def __lt__(self, other):
        return self.pos[1] < other.pos[1] or (self.pos[1] == other.pos[1] and self.pos[0] < other.pos[0])

    def __gt__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__le__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return not self.__eq__(other)


def battle_is_over(cavern: List[Node]) -> bool:
    return all(n.creature.dead() for n in cavern if isinstance(n.creature, Goblin)) \
           or all(n.creature.dead() for n in cavern if isinstance(n.creature, Elf))


def solve(puzzleinput):
    """
    Try to find minimal dps for which Elves win the battle without losses.
    Say required dps is 32. Start with 3, double it until we overshoot, then backtrack.

    dps                       fictive outcomes        left  right (boundaries before round)
    =======================================================================================
    3                         lose                    0     Inf
    3 * 2 = 6                 lose                    3     Inf
    6 * 2 = 12                win with losses         6     Inf
    12 * 2 = 24               win with losses         12    Inf
    24 * 2 = 48               win without losses      24    Inf
    48 - ((48-24)//2) = 36    win without losses      24    48
    36 - ((36-24)//2) = 30    win with losses         24    36
    30 + ((36-30)//2) = 33    win without losses      30    36
    33 - ((33-30)//2) = 31    win with losses         30    33
    31 + ((33-31)//2) = 32    win without losses      31    33
                                                      31    32    done - answer is upperbound
    """
    curr_elf_dps = Elf.dps
    lowerbound, upperbound = 0, math.inf
    elves = []
    rounds = 0
    while lowerbound < curr_elf_dps < upperbound:
        nodes = {}
        # Create graph nodes
        for y, row in enumerate([i.strip() for i in puzzleinput.splitlines() if i.strip()]):
            for x, cell in enumerate(row):
                if cell == '#': continue
                creature = {'G': Goblin, 'E': Elf}[cell](elf_dps=curr_elf_dps) if cell in 'GE' else None
                nodes[(x, y)] = Node((x, y), nodes, creature=creature)

        # Link nodes neighbors
        for node in nodes.values():
            for other in nodes.values():
                if node is other or other in node.neighbors:
                    continue
                if abs(node.pos[0] - other.pos[0]) + abs(node.pos[1] - other.pos[1]) == 1:  # MH Dist
                    node.neighbors.append(other)
                    other.neighbors.append(node)

        cavern = [node for node in nodes.values()]
        elves = [node.creature for node in cavern if isinstance(node.creature, Elf)]
        rounds = 0
        # Simulate the battle - "cheating" a little bit by dropping out when an elf dies.
        try:
            while True:
                last_action = 0
                for node in cavern:
                    last_action = node.evaluate(rounds)

                if last_action == 0 and (battle_is_over(cavern)):
                    break
                rounds += 1
        except AnElfHasDied:
            pass

        if all(i.dead() for i in elves):
            battle_result = 'elves lose'
        else:
            battle_result = 'elves won with losses' if any(i.dead() for i in elves) else 'elves flawless victory'
        print(f'{curr_elf_dps:5d}   {battle_result:24s}  {lowerbound:5d}  {upperbound:5}')

        if any(elf.dead() for elf in elves):
            # if any elf died, we must give them more power!
            lowerbound = curr_elf_dps
            if upperbound < math.inf:
                curr_elf_dps += (upperbound - lowerbound) // 2
            else:
                curr_elf_dps *= 2
        elif all(not elf.dead() for elf in elves):
            # all elves alive, maybe we are overkilling those gobbies
            upperbound = curr_elf_dps
            curr_elf_dps -= (upperbound - lowerbound) // 2

    answer = upperbound
    t_done = (time.time() - t_start) * 1000
    hitpoints = sum([elf.health for elf in elves])
    outcome = rounds * hitpoints
    print(f'Round {rounds}: remaining elf hitpoints {hitpoints} with dps {answer} and outcome {outcome}')
    print(f'Found in {t_done:.2f}ms')
    return outcome


def test():
    import glob
    results = []
    testfiles = glob.glob('input_*.txt')
    for test in testfiles:
        with open(test) as f:
            puzzleinput = f.read()
        expected_outcome = int(''.join(c for c in test if c.isdigit()))
        actual_outcome = solve(puzzleinput)
        results.append((test, expected_outcome, actual_outcome, actual_outcome - expected_outcome))
    for res in results:
        print(f'File: {res[0]:25s}  Expected: {res[1]}  Actual: {res[2]}   Diff: {res[3]:+}')


def part1():
    with open('input.txt') as f:
        puzzleinput = f.read()
    solve(puzzleinput)


if __name__ == '__main__':
    # test()
    part1()
