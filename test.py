import unittest
import numpy as np

import main
import configuration as CONFIG


class TestGeneticOperations(unittest.TestCase):
    def test_sample_population(self):
        CONFIG.POPULATION_SIZE = 9
        main.N = 3
        main.dist = np.array([
            [0, 20, 30],
            [20, 0, 60],
            [30, 60, 0]
        ])
        pop = np.array([
            [0, 1, 2],
            [1, 0, 2],
            [2, 0, 1],
            [0, 1, 2],
            [1, 0, 2],
            [2, 0, 1],
            [0, 1, 2],
            [1, 0, 2],
            [2, 0, 1]
        ])

        result = main.eval_population(pop)
        self.assertTrue(np.allclose(result, np.array([80, 50, 50, 80, 50, 50, 80, 50, 50])))

    def test_calculate_prob(self):
        """
        create random population, calculate scores, order population by scores ascending,
        then calculate probability, order population by probability descending, check if both orders are the same
        """
        N = CONFIG.NUM_OF_CITIES
        rng = np.random.default_rng(12345)
        x = np.arange(N)
        random_pop = rng.permuted(np.tile(x, CONFIG.POPULATION_SIZE).reshape(CONFIG.POPULATION_SIZE, x.size), axis=1)

        a = np.random.rand(N, N)
        random_dist = np.tril(a) + np.tril(a, -1).T
        random_dist[np.diag_indices(N, ndim=2)] = 0
        main.dist = random_dist

        scores = main.eval_population(random_pop)
        scores_idx = np.argsort(scores, kind='stable')

        prob = main.calculate_prob(scores)
        prob_idx = np.argsort(prob, kind='stable')
        prob_idx_desc = prob_idx[::-1]

        correct_order = np.array_equal(scores_idx, prob_idx_desc)
        self.assertTrue(correct_order)

