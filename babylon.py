from core.astar import AStar
from core.babylon_node import BabylonNode
import random
import time


def main():
    """Main function."""
    algorithm = AStar()
    initial = BabylonNode()
    goal = BabylonNode()

    levels = 10  # Neighbors deep levels.
    for i in range(levels):
        initial = random.choice(initial.neighbors())
    initial.parent = None
    initial.movement = None

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
