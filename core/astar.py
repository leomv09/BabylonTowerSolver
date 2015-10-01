import Queue


class AStar:

    """A* pathfinding algorithm."""

    def solve(self, initial, goal):
        """Get the path from an initial node to a goal node.

        parameters:
            [Node] initial -- The initial node.
            [Node] goal -- The goal node.

        return:
            [Node] The final node in the path.
        """
        open_set = Queue.PriorityQueue()
        open_set.put((0, initial))
        closed_set = set()
        current = None

        while not open_set.empty():
            current = open_set.get()[1]
            closed_set.add(current)

            if current == goal:
                break

            for neighbor in current.neighbors():
                if (neighbor not in closed_set):
                    open_set.put((neighbor.f(goal), neighbor))

        return current
