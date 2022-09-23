import unittest
from hrd import Stack


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

    def test_is_empty_returns_true_when_empty(self):
        sut = Stack([])

        result = sut.is_empty()

        self.assertTrue(result)

    def test_is_empty_returns_falls_when_non_empty(self):
        sut = Stack([1])

        result = sut.is_empty()

        self.assertFalse(result)
