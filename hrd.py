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


# Implicit heap with root at index=1
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

        min_item = self._items[self._ROOT_INDEX]

        self._items[self._ROOT_INDEX] = self._items[len(self._items) - 1]
        self._items.pop()
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
        item_to_bubble = self._items[curr_index]

        while curr_index < self.length():

            l_child_index = curr_index * 2
            r_child_index = l_child_index + 1

            # curr_index is a leaf
            if l_child_index > self.length():
                return
            # curr_index only has a left-child
            elif r_child_index > self.length():
                if item_to_bubble > self._items[l_child_index]:
                    self._items[curr_index] = self._items[l_child_index]
                    self._items[l_child_index] = item_to_bubble
                return
            # curr_index has both children
            else:
                l_child = self._items[l_child_index]
                r_child = self._items[r_child_index]

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

    def __repr__(self) -> str:
        return self._items.__str__()
