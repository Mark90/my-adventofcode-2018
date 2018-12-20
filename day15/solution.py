"""
19-12-2018  11:45
This looks like a shortest-path algorithm

~1200ms, Python 3.7, intel i7 870

"""
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Dict

t_start = time.time()


class Creature:
    health: int = 200
    dps: int = 3
    last_moved: int = None

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


class Elf(Creature):
    """Santa's little helpers"""


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
                print(f'Round {rounds} - {lowest_hp.creature} at {lowest_hp} died, removing it')
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
    """Build graph, link the nodes, start the fight"""
    nodes = {}
    for y, row in enumerate([i.strip() for i in puzzleinput.splitlines() if i.strip()]):
        for x, cell in enumerate(row):
            if cell == '#': continue
            creature = {'G': Goblin, 'E': Elf}[cell]() if cell in 'GE' else None
            nodes[(x, y)] = Node((x, y), nodes, creature=creature)

    for node in nodes.values():
        for other in nodes.values():
            if node is other or other in node.neighbors:
                continue
            if abs(node.pos[0] - other.pos[0]) + abs(node.pos[1] - other.pos[1]) == 1:  # MH Dist
                node.neighbors.append(other)
                other.neighbors.append(node)

    cavern = [node for node in nodes.values()]
    rounds = 0
    while True:
        last_action = 0
        for node in cavern:
            last_action = node.evaluate(rounds)

        if last_action == 0 and (battle_is_over(cavern)):
            break
        rounds += 1

    t_done = (time.time() - t_start) * 1000
    hitpoints = sum([node.creature.health for node in cavern if node.creature and not node.creature.dead()])
    outcome = rounds * hitpoints
    print(
        f'Round {rounds}: remaining hitpoints {hitpoints} and outcome {outcome}\nFound in {t_done:.2f}ms')
    return outcome


def test():
    import glob
    results = []
    for test in glob.glob('input_*.txt'):
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
    test()
    # part1()
