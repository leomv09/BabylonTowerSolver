from .node import Node
import util
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
        self.hash = hash(tuple((i, j, self.grid[i][j]) for (i, j) in itertools.product(range(self.rows), range(self.cols))))

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
        return self.hash == other.hash if isinstance(other, BabylonNode) else False

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

    def _gap_downward_movements(self):
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

    def _gap_upward_movements(self):
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

    def _gap_movements(self):
        """
        Get all movements the gap is able to do.

        return:
            [list] The total movements from up and downwards
        """
        gap_movements = self._gap_downward_movements()
        gap_movements.extend(self._gap_upward_movements())
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
        return 1

    def _nearest_row(self, index, element):
        max_delta = max(index + 1, self.rows - index)
        delta = 0

        while delta < max_delta:
            lower_index = index - delta
            if lower_index >= 0 and element in self.grid[lower_index]:
                return self.grid[lower_index]

            upper_index = index + delta
            if upper_index < self.rows and element in self.grid[upper_index]:
                return self.grid[upper_index]

            delta += 1

    def _nearest_col(self, index, element):
        max_delta = max(index + 1, self.cols - index)
        delta = 0

        while delta < max_delta:
            lower_index = index - delta
            if lower_index >= 0:
                lower_col = [self.grid[j][lower_index] for j in range(self.rows)]
                if element in lower_col:
                    return lower_col

            upper_index = index + delta
            if upper_index < self.cols:
                upper_col = [self.grid[j][upper_index] for j in range(self.rows)]
                if element in upper_col:
                    return upper_col

            delta += 1

    def _hx(self, other):
        """Get the row diference average between two BabylonNode.

        parameters:
            [BabylonNode] other -- The other node.
        """
        total_cost = 0

        for i in range(self.rows):
            row_cost = 0
            row1 = self.grid[i]
            row2 = other.grid[i]

            for idx1 in range(self.cols):
                row3 = row2  # if row1[idx1] in row2 else other._nearest_row(i, row1[idx1])
                try:
                    idx2 = util._find(row3, row1[idx1], idx1)
                    if idx1 + idx2 == self.cols:
                        row_cost += abs(idx1 - idx2)
                    else:
                        row_cost += min(abs(idx1 - idx2), abs(self.cols - idx1 - idx2))
                except ValueError:
                    row_cost += (self.cols * self.rows)

            total_cost += (row_cost / float(self.cols))

        return total_cost

    def _hy(self, other):
        """Get the column diference average between two BabylonNode.

        parameters:
            [BabylonNode] other -- The other node.
        """
        total_cost = 0

        for i in range(self.cols):
            col_cost = 0
            row1 = [self.grid[j][i] for j in range(self.rows)]
            row2 = [other.grid[j][i] for j in range(other.rows)]

            for idx1 in range(self.rows):
                row3 = row2  # if row1[idx1] in row2 else other._nearest_col(i, row1[idx1])
                try:
                    idx2 = util._find(row3, row1[idx1], idx1)
                    col_cost += abs(idx1 - idx2)
                except ValueError:
                    col_cost += (self.cols * self.rows)

            total_cost += (col_cost / float(self.rows))

        return total_cost

    def h(self, goal):
        """Get the heuristic estimate of the cost to get from this node to the goal node.

        parameters:
            [BabylonNode] goal -- The goal node.
        """
        return self._hx(goal) + self._hy(goal)

    def neighbors(self):
        """Get the neighbors nodes.

        return:
            [list] The list of neighbors.
        """
        return [self._apply(movement) for movement in self._valid_movements()]
