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
        open_set.put(initial, 0)
        closed_set = []
        current = None

        while not open_set.empty():
            current = open_set.get()
            closed_set.append(current)

            if current == goal:
                break

            for neighbor in current.neighbors():
                if (neighbor not in closed_set):
                    open_set.put(neighbor, neighbor.f(goal))

        return current
