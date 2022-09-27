from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
import heapq
from sys import argv
from typing import *


Grid = List[List[int]]
Cord = Tuple[int, int]


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
        old_cords = (self.row, self.col)

        for row_delta, col_delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_cords = (self.row + row_delta, self.col + col_delta)
            new_grid = self._move(grid, old_cords, new_cords)
            if new_grid:
                successors.append(new_grid)

        return successors

    def _move(self, grid: Grid, old_cords: Cord, new_cords: Cord) -> Optional[Grid]:

        for row in range(new_cords[0], new_cords[0] + self.rows):
            for col in range(new_cords[1], new_cords[1] + self.cols):

                if not row in range(len(grid)) or not col in range(len(grid[0])):
                    return None

                is_cell_empty = grid[row][col] == PieceType.EMPTY
                row_inside_piece = row in range(self.row, self.row + self.rows)
                col_inside_piece = col in range(self.col, self.col + self.cols)

                # we can overwrite current cell if its empty or belongs to this piece
                if not is_cell_empty and not (row_inside_piece and col_inside_piece):
                    return None

        copy = deepcopy(grid)
        self._fill(copy, old_cords, PieceType.EMPTY)
        self._fill(copy, new_cords, self.symbol)

        return copy

    def _fill(self, grid: Grid, top_left: Cord, symbol: int) -> Optional[Grid]:
        for row in range(top_left[0], top_left[0] + self.rows):
            for col in range(top_left[1], top_left[1] + self.cols):
                grid[row][col] = symbol


class State:

    id: str
    grid: Grid
    parent: Optional['State']
    cost: int = 0
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
        for row in puzzle_file.readlines():
            grid.append([int(char) for char in row.strip()])

    _load_output_symbol_map(grid)

    return grid


def _load_output_symbol_map(grid: Grid) -> None:

    pieces = generate_pieces(grid)

    for piece in pieces:
        if piece.symbol not in output_symbol_map:
            # horizontal piece
            if piece.rows < piece.cols:
                output_symbol_map[piece.symbol] = 2
            else:
                output_symbol_map[piece.symbol] = 3


def generate_pieces(grid: Grid) -> List[Piece]:

    pieces = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):

            cell = grid[row][col]
            piece: Piece = None

            if cell == PieceType.EMPTY:
                continue
            elif cell == PieceType.OneByOne:
                piece = Piece(1, 1, row, col, PieceType.OneByOne)
            elif cell == PieceType.TwoByTwo:
                piece = create_two_by_two(grid, row, col)
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


def is_goal_state(state: State) -> bool:
    for row, col in [(3, 1), (3, 1), (4, 2), (4, 2)]:
        if state.grid[row][col] != PieceType.TwoByTwo:
            return False

    return True


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


def main(input_filename: str, dfs_filename: str, a_star_filename: str) -> None:

    start_state = State(generate_grid(input_filename))
    dfs_goal = search(start_state, Stack(), lambda s: 0)

    if dfs_goal is None:
        print("DFS could not find a solution")
    else:
        dfs_cost, dfs_sol_path = recreate_start_to_goal_path(dfs_goal)
        write_path(dfs_filename, dfs_cost, dfs_sol_path)

    start_state = State(generate_grid(input_filename))
    a_star_goal = search(start_state, MinHeap(), manhattan_distance)

    if a_star_goal is None:
        print("A* could not find a solution")
    else:
        a_star_cost, a_star_sol_path = recreate_start_to_goal_path(a_star_goal)
        write_path(a_star_filename, a_star_cost, a_star_sol_path)


if __name__ == "__main__":

    if len(argv) != 4:
        print("Usage: python3 hrd.py  <input file>  <DFS output file>  <A* output file>")
        exit()

    main(
        input_filename=argv[1],
        dfs_filename=argv[2],
        a_star_filename=argv[3]
    )
