from copy import deepcopy
from sys import argv
from typing import *


Grid = List[List[int]]


class PieceType:
    EMPTY = 0
    OneByOne = 7
    TwoByTwo = 1


class Piece:
    def __init__(self, rows: int, cols: int, row: int, col: int, symbol: int) -> None:
        self.rows = rows
        self.cols = cols
        self.row = row
        self.col = col
        self.symbol = symbol

    def get_moves(self, grid: Grid) -> List[Grid]:
        successors = []
        successors += self._get_horizontal_moves(grid)
        successors += self._get_vertical_moves(grid)

        return successors

    def _get_horizontal_moves(self, grid: Grid) -> None:

        successors = []
        # (col_to_fill, col_to_remove)
        move_pairs = [
            (self.col - 1, self.col + self.cols - 1),
            (self.col + self.cols, self.col)
        ]

        for col_to_fill, col_to_remove in move_pairs:

            bottom_row = self.row + self.rows - 1

            if col_to_fill not in range(len(grid[self.row])):
                continue

            if grid[self.row][col_to_fill] == PieceType.EMPTY and grid[bottom_row][col_to_fill] == PieceType.EMPTY:

                copy = deepcopy(grid)

                copy[self.row][col_to_fill] = self.symbol
                copy[bottom_row][col_to_fill] = self.symbol
                copy[self.row][col_to_remove] = PieceType.EMPTY
                copy[bottom_row][col_to_remove] = PieceType.EMPTY

                successors.append(copy)

        return successors

    def _get_vertical_moves(self, grid: Grid) -> None:

        successors = []
        # (row_to_fill, row_to_remove)
        move_pairs = [
            (self.row - 1, self.row + self.rows - 1),
            (self.row + self.rows, self.row)
        ]

        for row_to_fill, row_to_remove in move_pairs:

            # x coord of right col of piece
            right_col = self.col + self.cols - 1

            if row_to_fill not in range(len(grid)):
                continue

            if grid[row_to_fill][self.col] == PieceType.EMPTY and grid[row_to_fill][right_col] == PieceType.EMPTY:

                copy = deepcopy(grid)

                copy[row_to_fill][self.col] = self.symbol
                copy[row_to_fill][right_col] = self.symbol
                copy[row_to_remove][self.col] = PieceType.EMPTY
                copy[row_to_remove][right_col] = PieceType.EMPTY

                successors.append(copy)

        return successors

    def __repr__(self) -> str:
        return f"{self.rows}x{self.cols} at ({self.row}, {self.col})"


class State:

    id: str
    grid: Grid
    parent: Optional['State']
    priority: int

    def __init__(self, grid: Grid, parent: Optional['State'] = None) -> None:
        self.grid = grid
        self.parent = parent
        self._generate_id()

    def get_successors(self) -> List['State']:

        pieces = self._generate_pieces()
        successors = []

        for piece in pieces:
            grids = piece.get_moves(self.grid)
            for grid in grids:
                successors.append(State(grid, self))

        return successors

    def _generate_id(self) -> None:
        self.id = ""
        for row in self.grid:
            for col in row:
                self.id += str(col)

    def _generate_pieces(self) -> List[Piece]:

        pieces = []

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):

                cell = self.grid[row][col]

                if cell == PieceType.EMPTY:
                    continue
                elif cell == PieceType.OneByOne:
                    pieces.append(Piece(1, 1, row, col, PieceType.OneByOne))
                elif cell == PieceType.TwoByTwo:
                    piece = create_two_by_two(self.grid, row, col)
                    if piece:
                        pieces.append(piece)
                else:
                    piece = create_one_by_two(self.grid, row, col)
                    if piece:
                        pieces.append(piece)

        return pieces

    def __repr__(self) -> str:
        grid_str = ""
        for row in self.grid:
            grid_str += str(row) + "\n"
        return grid_str


class Frontier:
    def add(self, state: State) -> None:
        pass

    def remove(self) -> State:
        pass

    def is_empty(self) -> bool:
        pass


class Stack(Frontier):

    _items = []

    def __init__(self, items: List[State] = []) -> None:
        self._items = items

    def add(self, item: State) -> None:
        self._items.append(item)

    def remove(self) -> State:
        if len(self._items) > 0:
            return self._items.pop()
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0


class MinHeap(Frontier):

    _ZERO_INDEX_PLACEHOLDER = None
    _ROOT_INDEX = 1

    def __init__(self) -> None:
        self._items = [self._ZERO_INDEX_PLACEHOLDER]

    def add(self, item: State) -> None:
        self._items.append(item)
        self._bubble_up()

    def remove(self) -> State:

        if self.length() == 0:
            return None
        if self.length() == 1:
            return self._items.pop()

        self._swap(self._ROOT_INDEX, len(self._items) - 1)
        min_item = self._items.pop()
        self._bubble_down()

        return min_item

    def is_empty(self) -> bool:
        return self.length() == 0

    def length(self) -> int:
        return len(self._items) - 1

    def _bubble_up(self):

        curr_index = len(self._items) - 1
        item_to_bubble = self._items[curr_index]

        while curr_index > self._ROOT_INDEX:

            parent_index = curr_index // 2
            parent = self._items[parent_index]

            if parent < item_to_bubble:
                return

            self._items[parent_index] = item_to_bubble
            self._items[curr_index] = parent
            curr_index = parent_index

    def _bubble_down(self):

        curr_index = self._ROOT_INDEX

        while curr_index < self.length():

            l_child_index = curr_index * 2
            r_child_index = l_child_index + 1

            # curr_index is a leaf
            if l_child_index > self.length():
                return
            # curr_index only has a left-child
            elif r_child_index > self.length():
                if self._items[curr_index] > self._items[l_child_index]:
                    self._swap(curr_index, l_child_index)
                return

            # curr_index has both children
            l_child = self._items[l_child_index]
            r_child = self._items[r_child_index]
            min_val = min(self._items[curr_index], l_child, r_child)

            if self._items[curr_index] == min_val:
                return
            elif l_child == min_val:
                self._swap(curr_index, l_child_index)
                curr_index = l_child_index
            else:
                self._swap(curr_index, r_child_index)
                curr_index = r_child_index

    def _swap(self, i1: int, i2: int) -> None:
        self._items[i1], self._items[i2] = self._items[i2], self._items[i1]

    def __repr__(self) -> str:
        return self._items.__str__()


def create_one_by_two(grid: Grid, row: int, col: int) -> Optional[Piece]:

    symbol = grid[row][col]

    # horizontal
    if col + 1 < len(grid[row]) and grid[row][col + 1] == symbol:
        return Piece(1, 2, row, col, symbol)
    # vertical
    if row + 1 < len(grid) and grid[row + 1][col] == symbol:
        return Piece(2, 1, row, col, symbol)

    return None


def create_two_by_two(grid: Grid, row: int, col: int) -> Optional[Piece]:

    deltas = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for delta_row, delta_col in deltas:

        n_row = row + delta_row
        n_col = col + delta_col

        if n_row not in range(len(grid)) or n_col not in range(len(grid[row])):
            return None
        if grid[n_row][n_col] != PieceType.TwoByTwo:
            return None

    return Piece(2, 2, row, col, PieceType.TwoByTwo)


def generate_grid(puzzle_file_name: str) -> List[List[int]]:

    with open(puzzle_file_name) as puzzle_file:

        char_grid = []
        rows = puzzle_file.readlines()

        for row in rows:
            char_grid.append([int(char) for char in row.strip()])

        return char_grid


def search(
    frontier: Frontier,
    heuristic_func: Callable[[State], int],
    initial_state: State
) -> Optional[State]:

    initial_state.priority = heuristic_func(initial_state)
    frontier.add(initial_state)
    explored: Dict[str, State] = {}

    while not frontier.is_empty():

        curr_state = frontier.remove()

        if curr_state.id not in explored:

            explored[curr_state.id] = curr_state

            if is_goal_state(curr_state):
                return curr_state

            for neighbour in curr_state.get_successors():
                neighbour.priority = heuristic_func(neighbour)
                frontier.add(neighbour)

    return None


def is_goal_state(state: State) -> bool:

    deltas = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for delta_row, delta_col in deltas:

        row = 3 + delta_row
        col = 1 + delta_col

        if state.grid[row][col] != PieceType.TwoByTwo:
            return False

    return True


def dfs(initial_state: State) -> Optional[State]:
    return search(
        Stack(),
        lambda x: 0,
        initial_state
    )


def recreate_start_to_goal_path(goal: State) -> Tuple[int, List[Grid]]:

    curr = goal
    stack = Stack([])

    step_count = 0
    grids = []

    while curr is not None:
        stack.add(curr.grid)
        step_count += 1
        curr = curr.parent

    while not stack.is_empty():
        grids.append(stack.remove())

    return step_count, grids


if __name__ == "__main__":

    # puzzle_file_name = argv[1]
    puzzle_file_name = "puzzle5.txt"

    grid = generate_grid(puzzle_file_name)
    initial_state = State(grid)
    goal = dfs(initial_state)
    steps, start_to_goal_path = recreate_start_to_goal_path(goal)
    print(steps)
