import unittest
from hrd import PieceType, generate_grid, State


class TestState(unittest.TestCase):
    def test_generate_grid_one_1x1_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 7, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = State(grid)._generate_pieces()

        self.assertEqual(1, len(pieces))
        self.assertEqual(1, pieces[0].rows)
        self.assertEqual(1, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(PieceType.OneByOne, pieces[0].symbol)

    def test_generate_grid_one_1x2_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = State(grid)._generate_pieces()

        self.assertEqual(1, len(pieces))
        self.assertEqual(1, pieces[0].rows)
        self.assertEqual(2, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(2, pieces[0].symbol)

    def test_generate_grid_one_2x1_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = State(grid)._generate_pieces()

        self.assertEqual(1, len(pieces))
        self.assertEqual(2, pieces[0].rows)
        self.assertEqual(1, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(2, pieces[0].symbol)

    def test_generate_grid_one_2x2_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = State(grid)._generate_pieces()

        self.assertEqual(1, len(pieces))
        self.assertEqual(2, pieces[0].rows)
        self.assertEqual(2, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(PieceType.TwoByTwo, pieces[0].symbol)

    def test_generate_grid_puzzle5(self):
        grid = generate_grid("puzzle5.txt")

        pieces = State(grid)._generate_pieces()

        self.assertEqual(10, len(pieces))


if __name__ == "__main__":
    unittest.main()
