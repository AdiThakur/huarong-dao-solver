import unittest
from hrd import MinHeap, State


def create_state(priority: int) -> State:
    state = State([])
    state.cost = priority
    state.hval = 0
    return state


class TestMinHeap(unittest.TestCase):

    def test_extract_min_single_item_heap_returns_min_key(self):
        sut = MinHeap()
        sut.add(create_state(1))

        min_key = sut.remove().get_priority()

        self.assertEqual(1, min_key)

    def test_extract_min_returns_min_key(self):
        sut = MinHeap()
        for key in range(5, 0, -1):
            sut.add(create_state(key))

        min_key = sut.remove().get_priority()

        self.assertEqual(1, min_key)

    def test_heap_sort(self):
        sut = MinHeap()
        keys = [5, 1, 6, 10, 2, 4, 3]
        for key in keys:
            sut.add(create_state(key))

        sorted_keys = []
        while sut.length() > 0:
            sorted_keys.append(sut.remove().get_priority())

        self.assertEqual(sorted(keys), sorted_keys)


if __name__ == "__main__":
    unittest.main()