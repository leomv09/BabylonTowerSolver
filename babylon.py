from core.astar import AStar
from core.babylon_node import BabylonNode
import random
import time


def main():
    """Main function."""
    algorithm = AStar()
    #initial = BabylonNode(grid=[['-','-','-','*'],['a','A','v','r'],['a','v','A','r'],['a','v','A','r'],['a','A','v','r']])
    #goal = BabylonNode(grid=[['-','-','-','*'],['a','v','A','r'],['a','v','A','r'],['a','v','A','r'],['a','v','A','r']])
    initial = BabylonNode()
    goal = BabylonNode()


    levels = 3  # Neighbors deep levels.
    for i in range(levels):
        initial = random.choice(initial.neighbors())
    initial.parent = None
    initial.movement = None

    """
    initial = BabylonNode(grid=[
        ['B', '-', '-', '-'],
        ['R', 'Y', 'R', 'G'],
        ['R', 'G', 'B', 'Y'],
        ['B', 'Y', 'Y', '*'],
        ['G', 'G', 'B', 'R']])
    """

    """
    initial = BabylonNode(grid=[
        ['*', '-', '-', '-'],
        ['R', 'G', 'B', 'Y'],
        ['R', 'B', 'G', 'Y'],
        ['R', 'G', 'B', 'Y'],
        ['R', 'G', 'B', 'Y']])
    """

    print "FROM", '\n', initial, '\n'
    print "TO", '\n', goal, '\n'

    t0 = time.time()
    movements = algorithm.movements_between(initial, goal)
    t1 = time.time()

    print "MOVEMENTS"
    for movement in movements:
        print(movement)
        initial = initial._apply(movement)

    print '\n', "TIME: ", t1 - t0
    assert(initial == goal)

if __name__ == "__main__":
    main()
