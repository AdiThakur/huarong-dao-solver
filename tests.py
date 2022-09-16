import unittest

from hrd import *


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


class TestGenerateGrid(unittest.TestCase):
    def test_proper_format_generates_correct_grid(self):
        expected_grid = [
            [2, 1, 1, 3],
            [2, 1, 1, 3],
            [4, 6, 6, 5],
            [4, 7, 7, 5],
            [7, 0, 0, 7]
        ]
        puzzle_file_name = "puzzle5.txt"

        result = generate_grid(puzzle_file_name)

        self.assertEqual(expected_grid, result)


if __name__ == '__main__':
    unittest.main()
