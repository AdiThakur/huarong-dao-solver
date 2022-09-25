import unittest
from hrd import *


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


class TestManhattanDistance(unittest.TestCase):
    def test_mhdist_goal_state_returns_0(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 1, 1, 9],
            [9, 1, 1, 9]
        ]

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

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(6, mh_dist)

    def test_mhdist_state_left_of_goal_returns_correct_dist(self):
        grid = [
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [1, 1, 9, 9],
            [1, 1, 9, 9],
            [9, 9, 9, 9]
        ]

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

        mh_dist = manhattan_distance(State(grid))

        self.assertEqual(3, mh_dist)


if __name__ == "__main__":
    unittest.main()
