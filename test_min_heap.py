import unittest
from hrd import MinHeap


class TestMinHeap(unittest.TestCase):

    def test_extract_min_empty_heap_returns_none(self):
        sut = MinHeap()

        result = sut.remove()

        self.assertIsNone(result)

    def test_extract_min_single_item_heap_returns_item(self):
        sut = MinHeap()
        sut.add(1)

        result = sut.remove()

        self.assertEqual(1, result)

    def test_extract_min_returns_smallest_item(self):
        sut = MinHeap()
        for i in range(5, 0, -1):
            sut.add(i)

        result = sut.remove()

        self.assertEqual(1, result)

    def test_heap_sort(self):
        sut = MinHeap()
        items = [5, 1, 6, 10, 2, 4, 3]
        for item in items:
            sut.add(item)

        result = []
        while sut.length() > 0:
            result.append(sut.remove())

        self.assertEqual(sorted(items), result)
