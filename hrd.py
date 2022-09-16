class Stack:

    _items = []

    def __init__(self, items=[]):
        self._items = items

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if len(self._items) > 0:
            return self._items.pop()
        return None


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
