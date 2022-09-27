from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
import heapq
from sys import argv
from typing import *


Grid = List[List[int]]


output_symbol_map = {
    0: 0,
    1: 1,
    7: 4
}


class PieceType:
    EMPTY = 0
    OneByOne = 7
    TwoByTwo = 1


class Piece:
    def __init__(
        self, rows: int, cols: int, row: int, col: int, symbol: int
    ) -> None:
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
    cost: int = 0
    # Estimated cost from this state to goal
    hval: int = 0

    def __init__(self, grid: Grid, parent: Optional['State'] = None) -> None:
        self.grid = grid
        self.parent = parent
        self._generate_id()

    def get_priority(self) -> int:
        return self.cost + self.hval

    def get_successors(self) -> List['State']:

        pieces = generate_pieces(self.grid)
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
                self.id += str(output_symbol_map[col])

    def __repr__(self) -> str:
        grid_str = ""
        for row in self.grid:
            grid_str += str(row) + "\n"
        return grid_str


class Frontier(ABC):
    @abstractmethod
    def add(self, state: State) -> None:
        pass

    @abstractmethod
    def remove(self) -> State:
        pass

    @abstractmethod
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


@dataclass(order=True)
class MinHeapItem:
    priority: int
    item: State = field(compare=False)


class MinHeap(Frontier):

    _items: List[State]

    def __init__(self) -> None:
        self._items = []

    def add(self, state: State) -> None:
        heapq.heappush(
            self._items,
            MinHeapItem(priority=state.get_priority(), item=state)
        )

    def remove(self) -> State:
        return heapq.heappop(self._items).item

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def length(self) -> int:
        return len(self._items)


def generate_grid(puzzle_file_name: str) -> List[List[int]]:

    grid = []

    with open(puzzle_file_name) as puzzle_file:

        rows = puzzle_file.readlines()

        for row in rows:
            grid.append([int(char) for char in row.strip()])

    _load_output_symbol_map(grid)

    return grid


def _load_output_symbol_map(grid: Grid) -> None:

    pieces = generate_pieces(grid)

    for piece in pieces:

        if piece.symbol in output_symbol_map:
            continue

        # 1x2
        if piece.rows < piece.cols:
            output_symbol_map[piece.symbol] = 2
        # 2x1
        else:
            output_symbol_map[piece.symbol] = 3


def generate_pieces(grid: Grid) -> List[Piece]:

    pieces = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):

            cell = grid[row][col]

            if cell == PieceType.EMPTY:
                continue
            elif cell == PieceType.OneByOne:
                pieces.append(Piece(1, 1, row, col, PieceType.OneByOne))
            elif cell == PieceType.TwoByTwo:
                piece = create_two_by_two(grid, row, col)
                if piece:
                    pieces.append(piece)
            else:
                piece = create_one_by_two(grid, row, col)
                if piece:
                    pieces.append(piece)

    return pieces


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


def is_goal_state(state: State) -> bool:

    deltas = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for delta_row, delta_col in deltas:

        row = 3 + delta_row
        col = 1 + delta_col

        if state.grid[row][col] != PieceType.TwoByTwo:
            return False

    return True


def manhattan_distance(state: State) -> int:

    pieces = generate_pieces(state.grid)

    for piece in pieces:
        if piece.symbol == PieceType.TwoByTwo:

            if is_goal_state(state):
                return 0

            vert_dist = abs(3 - piece.row)
            hori_dist = abs(1 - piece.col)

            return vert_dist + hori_dist

    # max valid vertical + horizontal
    return 4


def search(
    start: State,
    frontier: Frontier,
    heauristic_func: Callable[[State], int]
) -> Optional[State]:

    start.cost = 0
    start.hval = heauristic_func(start)

    frontier.add(start)
    explored: Dict[str, State] = {}

    while not frontier.is_empty():

        curr_state = frontier.remove()

        if curr_state.id not in explored:

            explored[curr_state.id] = curr_state

            if is_goal_state(curr_state):
                return curr_state

            for neighbour in curr_state.get_successors():
                neighbour.cost = curr_state.cost + 1
                neighbour.hval = manhattan_distance(neighbour)
                frontier.add(neighbour)

    return None


def recreate_start_to_goal_path(goal: State) -> Tuple[int, List[State]]:

    curr_state = goal
    stack = Stack([])

    path = []

    while curr_state is not None:
        stack.add(curr_state)
        curr_state = curr_state.parent

    while not stack.is_empty():
        path.append(stack.remove())

    return len(path) - 1, path


def write_path(filename: str, cost: int, path: List[State]) -> None:

    with open(filename, mode='w') as f:
        f.write(f"Cost of the solution: {cost}\n")

        for state in path:
            grid_str = ""
            for row in state.grid:
                row_str = ""
                for col in row:
                    row_str += str(output_symbol_map[col])
                grid_str += row_str + "\n"
            f.write(grid_str + "\n")


def main(
    input_filename: str,
    dfs_output_filename: str,
    a_star_output_filename: str
) -> None:

    dfs_initial_state = State(generate_grid(input_filename))
    dfs_goal = search(
        start=dfs_initial_state,
        frontier=Stack(),
        heauristic_func=lambda x: 0
    )

    if dfs_goal is None:
        print("DFS could not find a solution")
    else:
        dfs_steps, dfs_sol_path = recreate_start_to_goal_path(dfs_goal)
        write_path(
            filename=dfs_output_filename,
            cost=dfs_steps,
            path=dfs_sol_path
        )

    a_star_initial_state = State(generate_grid(input_filename))
    a_star_goal = search(
        start=a_star_initial_state,
        frontier=MinHeap(),
        heauristic_func=manhattan_distance
    )

    if a_star_goal is None:
        print("A* could not find a solution")
    else:
        a_star_steps, a_star_sol_path = recreate_start_to_goal_path(a_star_goal)
        write_path(
            filename=a_star_output_filename,
            cost=a_star_steps,
            path=a_star_sol_path
        )


if __name__ == "__main__":

    if len(argv) != 4:
        print("Usage: python3 hrd.py  <input file>  <DFS output file>  <A* output file>")
        exit()

    main(
        input_filename=argv[1],
        dfs_output_filename=argv[2],
        a_star_output_filename=argv[3]
    )
