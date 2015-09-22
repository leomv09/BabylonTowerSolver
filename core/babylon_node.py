from .node import Node
import copy
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
            grid=[['*', '-', '-', '-'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y'], ['R', 'G', 'B', 'Y']],
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
        self.gap_index = self._gap_index()

    def __eq__(self, other):
        """Check if this node is equal to other node.

        parameter:
            [BabylonNode] other -- The other node.

        return:
            [bool] True if this node have the same grid as the other node.
        """
        return self.grid == other.grid if isinstance(other, BabylonNode) else False

    def __repr__(self):
        """Get the string representation of this node.

        return:
            [string] The grid as a matrix.
        """
        res = '\n'.join(map(str, self.grid))
        return re.sub("[\[|\]|,|']", "", res)

    def _gap_index(self):
        """Get the index of the gap cell.

        return:
            [tuple] The index of the gap cell as an (x, y) tuple.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if (self.grid[i][j] == '*'):
                    return (i, j)
        return None

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
        direction = movement[0]
        row = movement[1]
        mul = movement[2]
        grid = copy.deepcopy(self.grid)

        if (row == '*'):
            # Gap movement
            x = self.gap_index[0]
            y = self.gap_index[1]
            for i in range(mul):
                if (direction == 'R'):
                    grid[x][y], grid[x][(y + 1) % self.cols] = grid[x][(y + 1) % self.cols], grid[x][y]
                    y = (y + 1) % self.cols
                elif (direction == 'L'):
                    grid[x][y], grid[x][(y - 1) % self.cols] = grid[x][(y - 1) % self.cols], grid[x][y]
                    y = (y - 1) % self.cols
                elif (direction == 'U'):
                    grid[x][y], grid[(x - 1) % self.rows][y] = grid[(x - 1) % self.rows][y], grid[x][y]
                    x = (x - 1) % self.rows
                elif (direction == 'D'):
                    grid[x][y], grid[(x + 1) % self.rows][y] = grid[(x + 1) % self.rows][y], grid[x][y]
                    x = (x + 1) % self.rows
                else:
                    raise ValueError("Invalid movement " + str(movement))
        else:
            # Row movement
            if (direction == 'R'):
                grid[row] = grid[row][-(mul % self.cols):] + grid[row][:-(mul % self.cols)]
            elif (direction == 'L'):
                grid[row] = grid[row][(mul % self.cols):] + grid[row][:(mul % self.cols)]
            else:
                raise ValueError("Invalid movement " + str(movement))

        return BabylonNode(grid, self, movement)

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
