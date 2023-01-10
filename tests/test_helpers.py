import unittest
from hrd import *
from hrd import _load_output_symbol_map


TEST_PUZZLE = "test_puzzle.txt"


class TestGenerateGrid(unittest.TestCase):
    def test_proper_format_generates_correct_grid(self):
        expected_grid = [
            [2, 1, 1, 3],
            [2, 1, 1, 3],
            [4, 6, 6, 5],
            [4, 7, 7, 5],
            [7, 0, 0, 7]
        ]
        puzzle_file_name = TEST_PUZZLE

        result = generate_grid(puzzle_file_name)

        self.assertEqual(expected_grid, result)


class TestGeneratePieces(unittest.TestCase):
    def test_generate_pieces_one_1x1_in_grid(self):
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

    def test_generate_pieces_one_1x2_in_grid(self):
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

    def test_generate_pieces_one_2x1_in_grid(self):
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

    def test_generate_pieces_one_2x2_in_grid(self):
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

    def test_generate_grid_puzzle5(self):
        grid = generate_grid(TEST_PUZZLE)

        pieces = generate_pieces(grid)

        self.assertEqual(10, len(pieces))


class TestIsGoalState(unittest.TestCase):
    def test_is_goal_state_2x2_above_exit_returns_true(self):
        grid = [
            [2, 7, 7, 3],
            [2, 7, 7, 3],
            [4, 6, 6, 5],
            [4, 1, 1, 5],
            [7, 1, 1, 7]
        ]

        result = is_goal_state(State(grid))

        self.assertTrue(result)

    def test_is_goal_state_2x2_not_above_exit_returns_false(self):
        grids = [
            [
                [2, 7, 7, 3],
                [2, 7, 7, 3],
                [4, 6, 6, 5],
                [1, 1, 6, 5],
                [1, 1, 6, 7]
            ],
            [
                [2, 7, 7, 3],
                [2, 7, 7, 3],
                [4, 6, 6, 5],
                [6, 6, 1, 1],
                [6, 6, 1, 1]
            ],
            [
                [2, 7, 7, 3],
                [2, 7, 7, 3],
                [4, 1, 1, 5],
                [6, 1, 1, 6],
                [6, 6, 6, 6]
            ]
        ]

        for grid in grids:
            result = is_goal_state(State(grid))
            self.assertFalse(result)


class TestManhattanDistance(unittest.TestCase):
    def test_mhdist_goal_state_returns_0(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 1, 1, 9],
            [9, 1, 1, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(0, mh_dist)

    def test_mhdist_invalid_state_returns_max_dist(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(4, mh_dist)

    def test_mhdist_state_left_of_goal_returns_correct_dist(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [1, 1, 9, 9],
            [1, 1, 9, 9],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(2, mh_dist)

    def test_mhdist_state_right_of_goal_returns_correct_dist(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 1, 1],
            [9, 9, 1, 1],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(2, mh_dist)

    def test_mhdist_state_above_goal_returns_correct_dist(self):
        grid = [
            [9, 1, 1, 9],
            [9, 1, 1, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(3, mh_dist)

    def test_mhdist_state_NW_of_goal_returns_correct_dist(self):
        grid = [
            [1, 1, 0, 9],
            [1, 1, 0, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(4, mh_dist)

    def test_mhdist_state_NE_of_goal_returns_correct_dist(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 1, 1],
            [9, 9, 1, 1],
            [9, 9, 9, 9],
            [9, 9, 9, 9]
        ]
        _load_output_symbol_map(grid)

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(3, mh_dist)


class TestLoadOutputSymbolMap(unittest.TestCase):
    def test_symbols_mapped_correctly(self):

        generate_grid(TEST_PUZZLE)

        self.assertEqual(0, output_symbol_map[0])
        self.assertEqual(4, output_symbol_map[7])
        self.assertEqual(1, output_symbol_map[1])

        # 2x1
        self.assertEqual(2, output_symbol_map[6])

        # 1x2
        self.assertEqual(3, output_symbol_map[2])
        self.assertEqual(3, output_symbol_map[3])
        self.assertEqual(3, output_symbol_map[4])
        self.assertEqual(3, output_symbol_map[5])


if __name__ == "__main__":
    unittest.main()
