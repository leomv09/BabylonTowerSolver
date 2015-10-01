from core.astar import AStar
from core.babylon_node import BabylonNode
import random
import time


def main():
    """Main function."""
    algorithm = AStar()
    n1 = BabylonNode()
    n2 = BabylonNode()

    levels = 1  # Neighbors deep levels.
    for i in range(levels):
        n1 = random.choice(n1.neighbors())

    print "FROM", '\n', n1, '\n'
    print "TO", '\n', n2, '\n'

    t0 = time.time()
    n3 = algorithm.solve(n1, n2)
    t1 = time.time()

    movements = []
    while n3.parent is not None:
        movements.append(n3.movement)
        n3 = n3.parent
    movements.reverse()

    print "MOVEMENTS"
    for movement in movements:
        print(movement)

    print '\n', "TIME: ", t1 - t0

if __name__ == "__main__":
    main()
