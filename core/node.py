class Node:

    """A node in the A* expansion tree.

    attributes:
        [Node] parent -- The parent node.
    """

    def __init__(self, parent=None):
        """Create a Node.

        parameters:
            [Node] parent -- The parent node.
        """
        self.parent = parent

    def cost(self):
        """Get the cost of getting from the parent node to this node."""
        raise NotImplementedError()

    def f(self, goal):
        """Get the total cost of this node.

        parameters:
            [Node] goal -- The goal node.
        """
        return self.g() + self.h(goal)

    def g(self):
        """Get the cost of getting from the initial node to this node."""
        return 0 if self.parent is None else self.parent.g() + self.cost()

    def h(self, goal):
        """Get the heuristic estimate of the cost to get from this node to the goal node.

        parameters:
            [Node] goal -- The goal node.
        """
        raise NotImplementedError()

    def neighbors(self):
        """Get the neighbors nodes.

        return:
            [list] The list of neighbors.
        """
        raise NotImplementedError()
