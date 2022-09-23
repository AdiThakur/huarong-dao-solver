import unittest
from hrd import PieceType, generate_grid, State, is_goal_state


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


if __name__ == "__main__":
    unittest.main()
