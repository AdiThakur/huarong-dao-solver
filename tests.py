import unittest

from hrd import MinHeap, Stack


@unittest.skip("Cuz")
class TestStack(unittest.TestCase):

    def test_pop_returns_last_pushed_item(self):
        sut = Stack([])
        for i in range(5):
            sut.push(i)

        result = sut.pop()

        self.assertEqual(4, result)

    def test_empty_stack_pop_returns_none(self):
        sut = Stack([])

        result = sut.pop()

        self.assertIsNone(result)


class TestMinHeap(unittest.TestCase):

    def test_extract_min_empty_heap_returns_none(self):
        sut = MinHeap()

        result = sut.extract_min()

        self.assertIsNone(result)

    def test_extract_min_single_item_heap_returns_item(self):
        sut = MinHeap()
        sut.add(1)

        result = sut.extract_min()

        self.assertEqual(1, result)

    def test_extract_min_returns_smallest_item(self):
        sut = MinHeap()
        for i in range(5, 0, -1):
            sut.add(i)

        result = sut.extract_min()

        self.assertEqual(1, result)

    def test_heap_sort(self):
        sut = MinHeap()
        items = [5, 1, 6, 10, 2, 4, 3]
        for item in items:
            sut.add(item)

        result = []
        while sut.length() > 0:
            result.append(sut.extract_min())

        self.assertEqual(sorted(items), result)


if __name__ == '__main__':
    unittest.main()
