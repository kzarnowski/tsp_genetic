import unittest
import numpy as np

import main


class TestEvalPopulation(unittest.TestCase):
    def test_sample_population(self):
        main.N = 3
        main.dist = np.array([
            [0, 20, 30],
            [20, 0, 60],
            [30, 60, 0]
        ])
        pop = np.array([
            [0, 1, 2],
            [1, 0, 2],
            [2, 0, 1]
        ])

        result = main.eval_population(pop)
        self.assertTrue(np.allclose(result, np.array([80, 50, 50])))

