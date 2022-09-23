from typing import *
import unittest
from hrd import Grid, Piece


def grid_diff(grid1: Grid, grid2: Grid) -> List[Tuple[int, int]]:

    diff_coords = []

    for x in range(len(grid1)):
        for y in range(len(grid1[x])):
            if grid1[x][y] != grid2[x][y]:
                diff_coords.append((x, y))

    return diff_coords


class Test1x1Piece(unittest.TestCase):
    def test_get_successors_ignores_center_and_diagonals(self):
        initial_state = [
            [0, 9, 0],
            [9, 8, 9],
            [0, 9, 0],
        ]
        sut = Piece(rows=1, cols=1, row=1, col=1, symbol=8)

        successors = sut.get_moves(initial_state)

        for successor in successors:
            self.assertEqual(0, successor[0][0])
            self.assertEqual(0, successor[0][2])
            self.assertEqual(0, successor[1][1])
            self.assertEqual(0, successor[2][0])
            self.assertEqual(0, successor[2][2])

    def test_get_successors_considers_all_open_spots(self):
        initial_state = [
            [9, 0, 9],
            [0, 8, 0],
            [9, 0, 9],
        ]
        sut = Piece(rows=1, cols=1, row=1, col=1, symbol=8)

        successors = sut.get_moves(initial_state)

        for successor in successors:
            self.assertNotEqual(initial_state, successor)
            self.assertEqual(2, len(grid_diff(initial_state, successor)))


class Test1x2Piece(unittest.TestCase):
    def test_get_successors_returns_empty_when_no_free_spots(self):
        initial_state = [
            [9, 0, 9, 0],
            [9, 1, 1, 9],
            [0, 0, 9, 0],
            [9, 9, 0, 9],
            [9, 9, 9, 9]
        ]
        sut = Piece(rows=1, cols=2, row=1, col=1, symbol=1)

        successors = sut.get_moves(initial_state)

        self.assertEqual(0, len(successors))

    def test_get_successors_returns_one_successor_when_one_spot_available(self):

        initial_and_expected = [
            # Free spot to the right
            (
                [
                    [0, 0, 9, 0],
                    [9, 1, 1, 0],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 0, 9, 0],
                    [9, 0, 1, 1],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot to the left
            (
                [
                    [0, 0, 9, 0],
                    [0, 1, 1, 9],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 0, 9, 0],
                    [1, 1, 0, 9],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot above
            (
                [
                    [0, 0, 0, 0],
                    [9, 1, 1, 9],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 1, 1, 0],
                    [9, 0, 0, 9],
                    [0, 9, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
            ),
            # Free spot below
            (
                [
                    [0, 9, 9, 0],
                    [9, 1, 1, 9],
                    [0, 0, 0, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 9, 9, 0],
                    [9, 0, 0, 9],
                    [0, 1, 1, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
            ),
        ]

        for initial, expected in initial_and_expected:

            sut = Piece(rows=1, cols=2, row=1, col=1, symbol=1)

            successors = sut.get_moves(initial)

            self.assertEqual(1, len(successors))
            self.assertEqual(expected, successors[0])


class Test2x1Piece(unittest.TestCase):
    def test_get_successors_returns_empty_when_no_free_spots(self):
        initial_state = [
            [0, 9, 0, 0],
            [9, 1, 0, 9],
            [0, 1, 9, 0],
            [0, 9, 0, 9],
            [9, 9, 9, 9]
        ]
        sut = Piece(rows=1, cols=2, row=1, col=1, symbol=1)

        successors = sut.get_moves(initial_state)

        self.assertEqual(0, len(successors))

    def test_get_successors_returns_one_successor_when_one_spot_available(self):

        initial_and_expected = [
            # Free spot to the right
            (
                [
                    [0, 9, 9, 0],
                    [9, 1, 0, 0],
                    [0, 1, 0, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 9, 9, 0],
                    [9, 0, 1, 0],
                    [0, 0, 1, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot to the left
            (
                [
                    [0, 9, 9, 0],
                    [0, 1, 9, 0],
                    [0, 1, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 9, 9, 0],
                    [1, 0, 9, 0],
                    [1, 0, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot above
            (
                [
                    [0, 0, 9, 0],
                    [9, 1, 9, 0],
                    [9, 1, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 1, 9, 0],
                    [9, 1, 9, 0],
                    [9, 0, 9, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
            ),
            # Free spot below
            (
                [
                    [0, 9, 9, 0],
                    [9, 1, 9, 0],
                    [9, 1, 9, 0],
                    [9, 0, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [0, 9, 9, 0],
                    [9, 0, 9, 0],
                    [9, 1, 9, 0],
                    [9, 1, 0, 9],
                    [9, 9, 9, 9]
                ],
            ),
        ]

        for initial, expected in initial_and_expected:

            sut = Piece(rows=2, cols=1, row=1, col=1, symbol=1)

            successors = sut.get_moves(initial)

            self.assertEqual(1, len(successors))
            self.assertEqual(expected, successors[0])


class Test2x2Piece(unittest.TestCase):
    def test_get_successors_returns_empty_when_no_free_spots(self):
        initial_state = [
            [9, 0, 9, 9],
            [9, 1, 1, 0],
            [0, 1, 1, 9],
            [9, 9, 0, 9],
            [9, 9, 9, 9]
        ]
        sut = Piece(rows=2, cols=2, row=1, col=1, symbol=1)

        successors = sut.get_moves(initial_state)

        self.assertEqual(0, len(successors))

    def test_get_successors_returns_one_successor_when_one_spot_available(self):

        initial_and_expected = [
            # Free spot to the right
            (
                [
                    [9, 0, 9, 9],
                    [9, 1, 1, 0],
                    [0, 1, 1, 0],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [9, 0, 9, 9],
                    [9, 0, 1, 1],
                    [0, 0, 1, 1],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot to the left
            (
                [
                    [9, 0, 9, 9],
                    [0, 1, 1, 9],
                    [0, 1, 1, 9],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [9, 0, 9, 9],
                    [1, 1, 0, 9],
                    [1, 1, 0, 9],
                    [9, 9, 0, 9],
                    [9, 9, 9, 9]
                ]
            ),
            # Free spot above
            (
                [
                    [9, 0, 0, 9],
                    [9, 1, 1, 9],
                    [9, 1, 1, 9],
                    [9, 9, 9, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [9, 1, 1, 9],
                    [9, 1, 1, 9],
                    [9, 0, 0, 9],
                    [9, 9, 9, 9],
                    [9, 9, 9, 9]
                ],
            ),
            # Free spot below
            (
                [
                    [9, 9, 9, 9],
                    [9, 1, 1, 9],
                    [9, 1, 1, 9],
                    [9, 0, 0, 9],
                    [9, 9, 9, 9]
                ],
                [
                    [9, 9, 9, 9],
                    [9, 0, 0, 9],
                    [9, 1, 1, 9],
                    [9, 1, 1, 9],
                    [9, 9, 9, 9]
                ],
            ),
        ]

        for initial, expected in initial_and_expected:

            sut = Piece(rows=2, cols=2, row=1, col=1, symbol=1)

            successors = sut.get_moves(initial)

            self.assertEqual(1, len(successors))
            self.assertEqual(expected, successors[0])


if __name__ == "__main__":
    unittest.main()
