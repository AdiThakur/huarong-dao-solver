class Stack:

    _items = []

    def __init__(self, items):
        self._items = items

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if len(self._items) > 0:
            return self._items.pop()
        return None


# Implicit heap with root at index=1
class MinHeap:

    _ROOT_INDEX = 1
    _items = []

    def add(self, item):
        self._items.append(item)
        self._bubble_up(len(self._items) - 1)

    def extract_min(self):

        if len(self._items < 1):
            return None

        min_item = self._items[self._ROOT_INDEX]

        self._items[self._ROOT_INDEX] = self._items[len(self._items) - 1]
        self._items.pop()
        self._bubble_down()

        return min_item

    def _bubble_up(self, item_to_bubble_index):

        item_to_bubble = self._items[item_to_bubble_index]

        while item_to_bubble_index >= 1:

            parent_index = item_to_bubble_index // 2
            parent = self._items[parent_index]

            if item_to_bubble < parent:
                self._items[parent_index] = item_to_bubble
                self._items[item_to_bubble] = parent
                item_to_bubble_index = parent_index
            else:
                return

    def _bubble_down(self):

        curr_index = self._ROOT_INDEX
        item_to_bubble = self._items[curr_index]

        while curr_index < len(self._items):

            l_child, l_child_index = self.get_left_child(curr_index)
            r_child, r_child_index = self.get_right_child(curr_index)

            # min-heap property is preserved
            if item_to_bubble <= l_child and item_to_bubble <= r_child:
                return

            if l_child < r_child:
                self._items[curr_index] = l_child
                self._items[l_child_index] = item_to_bubble
                curr_index = l_child_index
            else:
                self._items[curr_index] = r_child
                self._items[r_child_index] = item_to_bubble
                curr_index = r_child_index

    def get_left_child(self, parent_index: int):

        if parent_index < self._ROOT_INDEX or parent_index >= len(self._items):
            return None

        l_child_index = parent_index * 2

        if l_child_index >= len(self._items):
            return None

        return self._items[l_child_index], l_child_index

    def get_right_child(self, parent_index: int):

        if parent_index < self._ROOT_INDEX or parent_index >= len(self._items):
            return None

        r_child_index = (parent_index * 2) + 1

        if r_child_index >= len(self._items):
            return None

        return self._items[r_child_index], r_child_index
