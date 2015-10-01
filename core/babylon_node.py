from .node import Node
import itertools
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
            grid=[
                ['*', '-', '-', '-'],
                ['R', 'G', 'B', 'Y'],
                ['R', 'G', 'B', 'Y'],
                ['R', 'G', 'B', 'Y'],
                ['R', 'G', 'B', 'Y']],
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
        self.hash = self._hash()

    def __hash__(self):
        """Get the hash code of this node."""
        return self.hash

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

    def _hash(self):
        return hash(frozenset(frozenset(row) for row in self.grid))

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

    def _default_movements(self):
        """Get the default movements for any BabylonNode.

        return:
            [list] Default movements for Left and Right shifts (Always the same movements)
        """
        default_movements = []
        for row in range(0, self.rows):
            for shifts in range(1, (self.cols / 2) + 1):
                default_movements.append(('R', row, shifts))
            for shifts in range(1, self.cols - (self.cols / 2)):
                default_movements.append(('L', row, shifts))
        return default_movements

    def _downward_movements(self):
        """Get the downwards movements for the gap if applies.

        return:
            [list] Downwards movements. Empty if can't go down.
        """
        downward_movements = []
        gap_row = self.gap_index[0]
        rows_below = self.rows - gap_row

        for shifts in range(1, rows_below):
            downward_movements.append(('D', '*', shifts))
        return downward_movements

    def _upward_movements(self):
        """Get the upwards movements for the gap if applies avoiding any locked spot.

        return:
            [list] Upward movements. Empty if can't go Up.
        """
        upward_movements = []
        top_locked = self._top_locked()
        gap_row = self.gap_index[0]
        rows_above = gap_row + 1 if not top_locked else gap_row
        for shifts in range(1, rows_above):
            upward_movements.append(('U', '*', shifts))
        return upward_movements

    def _sidewards_movements(self):
        """Get the sidewars movements for the gap if applies.

        return:
            [list] Sidewards movements. Empty if the gap row is 0.
        """
        sidewards_movements = []
        gap_row = self.gap_index[0]

        if gap_row != 0:
            for shifts in range(1, (self.cols / 2) + 1):
                sidewards_movements.append(('R', '*', shifts))
            for shifts in range(1, self.cols - (self.cols / 2)):
                sidewards_movements.append(('L', '*', shifts))
        return sidewards_movements

    def _gap_movements(self):
        """
        Get all movements the gap is able to do.

        return:
            [list] The total movements from side, up and downwards
        """
        gap_movements = self._downward_movements()
        gap_movements.extend(self._upward_movements())
        gap_movements.extend(self._sidewards_movements())
        return gap_movements

    def _top_locked(self):
        gap_col = self.gap_index[1]
        return self.grid[0][gap_col] == '-'

    def _valid_movements(self):
        """Get all the movements that can be done from this node.

        return:
            [list] The list of valid movements.
        """
        valid_movements = self._default_movements()
        valid_movements.extend(self._gap_movements())
        return valid_movements

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
        return self.movement[2] if self.movement is not None else 0

    def _nearest_cell(self, indexes, index, cell):
        lower_cost = float("inf")
        lower_index = None
        x1, y1 = index[0], index[1]
        for value in indexes:
            x2, y2 = value[0], value[1]
            if (self.grid[x2][y2] == cell):
                cost = min(abs(y2 - y1), abs(self.cols - y2 - y1)) + abs(x2 - x1)
                if (cost < lower_cost):
                    lower_cost = cost
                    lower_index = value
        return lower_index, lower_cost

    def h(self, goal):
        """Get the heuristic estimate of the cost to get from this node to the goal node.

        parameters:
            [BabylonNode] goal -- The goal node.
        """
        indexes = [(x, y) for x, y in itertools.product(range(self.rows), range(self.cols))]
        value = 0

        for i in range(goal.rows):
            for j in range(goal.cols):
                cell = goal.grid[i][j]
                index, cost = self._nearest_cell(indexes, (i, j), cell)
                indexes.remove(index)
                value += cost

        return value / float(self.rows * self.cols)

    def neighbors(self):
        """Get the neighbors nodes.

        return:
            [list] The list of neighbors.
        """
        return [self._apply(movement) for movement in self._valid_movements()]
