import unittest
from hrd import Piece, PieceType, generate_grid, generate_pieces


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


class TestGeneratePieces(unittest.TestCase):
    def test_one_one_by_one_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 7, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = generate_pieces(grid)

        self.assertEqual(1, len(pieces))
        self.assertEqual(1, pieces[0].rows)
        self.assertEqual(1, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(PieceType.OneByOne, pieces[0].symbol)

    def test_one_one_by_two_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = generate_pieces(grid)

        self.assertEqual(1, len(pieces))
        self.assertEqual(1, pieces[0].rows)
        self.assertEqual(2, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(2, pieces[0].symbol)

    def test_one_two_by_one_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = generate_pieces(grid)

        self.assertEqual(1, len(pieces))
        self.assertEqual(2, pieces[0].rows)
        self.assertEqual(1, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(2, pieces[0].symbol)

    def test_one_two_by_two_in_grid(self):
        grid = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        pieces = generate_pieces(grid)

        self.assertEqual(1, len(pieces))
        self.assertEqual(2, pieces[0].rows)
        self.assertEqual(2, pieces[0].cols)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(1, pieces[0].row)
        self.assertEqual(PieceType.TwoByTwo, pieces[0].symbol)

    def test_puzzle5(self):
        grid = generate_grid("puzzle5.txt")

        pieces = generate_pieces(grid)

        self.assertEqual(10, len(pieces))


if __name__ == "__main__":
    unittest.main()
