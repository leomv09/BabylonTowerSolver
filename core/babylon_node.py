from .node import Node
import re


class BabylonNode(Node):

    """A node in the Babylon Tower Puzzle tree.

    attributes:
        [list] grid -- The data grid.
        [BabylonNode] parent -- The parent node.
        [tuple] movement -- The movement used to go from parent node to this node.
    """

    def __init__(
            self,
            grid=[['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['*', '-', '-', '-']],
            parent=None,
            movement=None):
        """Create a BabylonNode.

        parameters:
            [list] grid -- The data grid.
            [BabylonNode] parent -- The parent node.
            [tuple] movement -- The movement used to go from parent node to this node.
        """
        self.grid = grid
        self.parent = parent
        self.movement = movement
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def __eq__(self, other):
        """Check if this node is equal to other node.

        parameter:
            [BabylonNode] other -- The other node.

        return:
            True if this node have the same grid as the other node.
        """
        return self.grid == other.grid if isinstance(other, BabylonNode) else False

    def __repr__(self):
        """Get the string representation of this node.

        return:
            The grid as a matrix.
        """
        res = '\n'.join(map(str, reversed(self.grid)))
        return re.sub("[\[|\]|,|']", "", res)

    def _valid_movements(self):
        """Get all the movements that can be done from this node.

        return:
            [list] The list of valid movements.
        """
        return []

    def _apply(self, movement):
        """Get the resulting node by applying a movement to this node.

        parameters:
            [tuple] movement -- The movement to apply.

        return:
            [BabylonNode] The resulting node.
        """
        return None

    def cost(self):
        """Get the cost of getting from the parent node to this node."""
        return 0

    def h(self, goal):
        """Get the heuristic estimate of the cost to get from this node to the goal node.

        parameters:
            [BabylonNode] goal -- The goal node.
        """
        return 0

    def neighbors(self):
        """Get the neighbors nodes.

        return:
            [list] The list of neighbors.
        """
        return [self._apply(movement) for movement in self._valid_movements()]
