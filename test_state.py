import unittest
from hrd import State, _load_output_symbol_map


class TestState(unittest.TestCase): 
    def test_generate_id_equivalent_grids_produce_identical_ids(self):
        # Arrange
        puzzle5_config_grid = [
            [2, 1, 1, 3],
            [2, 1, 1, 3],
            [4, 6, 6, 5],
            [4, 7, 7, 5],
            [7, 0, 0, 7]
        ]
        _load_output_symbol_map(puzzle5_config_grid)

        # Act
        state1 = State(
            [
                [2, 1, 1, 3],
                [2, 1, 1, 3],
                [4, 6, 6, 5],
                [4, 7, 7, 5],
                [7, 0, 0, 7]
            ]
        )
        state2 = State(
            [
                [4, 1, 1, 5],
                [4, 1, 1, 5],
                [3, 6, 6, 2],
                [3, 7, 7, 2],
                [7, 0, 0, 7]
            ]
        )

        # Assert
        self.assertEqual(state1.id, state2.id)


if __name__ == "__main__":
    unittest.main()
