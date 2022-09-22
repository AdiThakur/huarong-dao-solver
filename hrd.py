from sys import argv
from typing import Any, List


class Stack:

    _items = []

    def __init__(self, items=[]) -> None:
        self._items = items

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if len(self._items) > 0:
            return self._items.pop()
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0


class MinHeap:

    _ZERO_INDEX_PLACEHOLDER = None
    _ROOT_INDEX = 1

    def __init__(self) -> None:
        self._items = [self._ZERO_INDEX_PLACEHOLDER]

    def add(self, item):
        self._items.append(item)
        self._bubble_up()

    def extract_min(self):

        if self.length() == 0:
            return None
        if self.length() == 1:
            return self._items.pop()

        self._swap(self._ROOT_INDEX, len(self._items) - 1)
        min_item = self._items.pop()
        self._bubble_down()

        return min_item

    def length(self) -> int:
        return len(self._items) - 1;

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


def generate_grid(puzzle_file_name: str) -> List[List[int]]:

    with open(puzzle_file_name) as puzzle_file:

        char_grid = []
        rows = puzzle_file.readlines()

        for row in rows:
            char_grid.append([int(char) for char in row.strip()])

        return char_grid


def dfs(initial_state: List[List[int]]):

    visited = set()
    frontier = Stack()
    frontier.push(initial_state)

    while not frontier.is_empty():

        curr_state = frontier.pop()

        if curr_state in visited:
            continue

        if is_goal_state(curr_state):
            return curr_state

        visited.add(curr_state)
        neighbours = get_successors(curr_state)
        for neighbour in neighbours:
            frontier.push(neighbour)

    return None


def is_goal_state(state) -> bool:
    pass

def get_successors(state):
    pass


if __name__ == "__main__":

    puzzle_file_name = argv[1]
    grid = generate_grid(puzzle_file_name)
    print(grid)