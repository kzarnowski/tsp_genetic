import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

import configuration as config

class GeneticAlgorithm():
    def __init__(self, config):
        self.config = config
        self.iters_without_change = 0
        self.best_idx = None
        self.best_score = None
        self.cities = None

    def set_cities(self, cities):
        self.cities = cities

    def run_algorithm(self):
        print("START")
        cities = self._generate_cities()
        N = cities.shape[0]
        dist = distance_matrix(cities, cities)

        population = self._init_population(N)
        scores = self._eval_population(population, dist)

        self.iters_without_change = 0
        self.best_idx = np.argmin(scores)
        self.best_score = scores[self.best_idx]

        gen = 0
        while not self._stop_condition(scores):
            if gen % 10 == 0:
                print(f"GEN: {gen} BEST: {self.best_score} SOLUTION: {population[self.best_idx]} ALL: {np.sum(scores)}")
            gen += 1

            parents = self._select_parents(population, scores)
            pairs = self._generate_pairs(parents)
            offspring = self._procreate(parents, pairs)

            offspring = self._mutate(offspring)

            population = self._next_generation(parents, offspring)
            scores = self._eval_population(population, dist)
    
    def _generate_cities(self):
        if config.RANDOM_MODE:
            x = np.random.uniform(0, config.WIDTH, config.NUM_OF_CITIES)
            y = np.random.uniform(0, config.HEIGHT, config.NUM_OF_CITIES)
            cities = np.column_stack((x, y))
        else:
            cities = np.loadtxt(config.CITIES_FILEPATH)
            #TODO: check file structure
        return cities

    def _init_population(self, N):
        rng = np.random.default_rng()
        x = np.arange(N, dtype=np.uint16)
        perms = rng.permuted(np.tile(x, config.POPULATION_SIZE).reshape(config.POPULATION_SIZE, x.size), axis=1)
        return perms


    def _eval_population(self, pop, dist):
        scores = np.empty(config.POPULATION_SIZE)
        rows = pop[:, :-1]
        cols = pop[:, 1:]
        for i in range(config.POPULATION_SIZE):
            scores[i] = np.sum(dist[rows[i], cols[i]])
        return scores


    def _calculate_prob(self, scores):
        total_cost = np.sum(scores)
        inv_ratio = total_cost / scores
        total_inv_ratio = np.sum(inv_ratio)
        return inv_ratio / total_inv_ratio


    def _select_parents(self, pop, scores):
        """
        Roulette-wheel method with inversed probability.
        """
        num_of_parents = int(config.PARENTS_RATIO * pop.shape[0])
        probabilities = self._calculate_prob(scores)

        indices = np.random.choice(
            range(pop.shape[0]),
            size=num_of_parents,
            replace=True,
            p=probabilities
        )
        parents = pop[indices, :]

        return parents

    @staticmethod
    def random_pair(max_value):
        rng = np.random.default_rng()
        idx = rng.choice(max_value, 2, replace=False)
        return idx[0], idx[1]


    def _generate_pairs(self, parents):
        if config.INCLUDE_PARENTS:
            offspring_size = config.POPULATION_SIZE - parents.shape[0]
        else:
            offspring_size = config.POPULATION_SIZE

        pairs = np.ndarray(shape=(offspring_size//2, 2), dtype=np.uint16)

        # TODO: remove loop
        for i in range(pairs.shape[0]):
            pairs[i, :] = self.random_pair(parents.shape[0])

        return pairs


    def _crossover(self, p1, p2):
        end = config.NUM_OF_CITIES - 1
        u, v = self.random_pair(end)

        if v < u:
            u, v = v, u
        if v - u < 2:
            v = min(v + 1, end)
            u = max(u - 1, 0)

        o1 = np.zeros(config.NUM_OF_CITIES, dtype=np.uint16)
        o2 = np.zeros(config.NUM_OF_CITIES, dtype=np.uint16)

        o1[u:v+1] = p1[u:v+1]
        o2[u:v+1] = p2[u:v+1]

        p1_rest = np.roll(p1, -(v+1))
        p2_rest = np.roll(p2, -(v+1))

        o1_fill = p2_rest[~np.in1d(p2_rest, o1[u:v+1])]
        o2_fill = p1_rest[~np.in1d(p1_rest, o2[u:v+1])]

        if v != end:
            o1[v+1:end+1] = o1_fill[:end-v]
            o2[v+1:end+1] = o2_fill[:end-v]

        if u != 0:
            o1[:u] = o1_fill[end-v:]
            o2[:u] = o2_fill[end-v:]

        return o1, o2


    def _mutate(self, pop):
        def mutate_individual(x):
            u, v = self.random_pair(x.shape[0])
            x[u], x[v] = x[v], x[u]
            return x

        def mutate_offsprings(offsprings):
            return np.apply_along_axis(mutate_individual, 1, offsprings)

        is_mutated = np.array(np.random.rand(pop.shape[0]) <= config.MUTATION_PROBABILITY)
        pop[is_mutated] = mutate_offsprings(pop[is_mutated])
        return pop


    def _procreate(self, parents, pairs):
        offspring = np.ndarray(shape=(
            2*pairs.shape[0],
            parents.shape[1]
        ), dtype=np.uint16)

        i = 0
        while i < 2*pairs.shape[0]:
            p1 = parents[pairs[i//2, 0], :]
            p2 = parents[pairs[i//2, 1], :]
            o1, o2 = self._crossover(p1, p2)
            offspring[i, :] = o1
            offspring[i+1, :] = o2
            i += 2
        return offspring


    def _next_generation(self, parents, offspring):
        if config.INCLUDE_PARENTS:
            return np.vstack((parents, offspring))
        else:
            return offspring

    def _stop_condition(self, scores):
        curr_best_idx = np.argmin(scores)
        curr_best_score = scores[curr_best_idx]

        if curr_best_score < self.best_score:
            self.best_score = curr_best_score
            self.best_idx = curr_best_idx
            self.iters_without_change = 0
            return False
        else:
            self.iters_without_change += 1
            return self.iters_without_change == config.MAX_ITER