import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from utils import random_pair

class GeneticAlgorithm():
    def __init__(self, config):
        self.config = config
        self.iters_without_change = 0
        self.best_idx = None
        self.cities = None

        self.is_stopped = True
        self.stats = dict.fromkeys(
            ["solution", "best_score", "avg_score", "generation_num"],
            None
        )

    def set_cities(self, cities):
        self.cities = cities

    def run_algorithm(self, progress_callback):
        print(self.config)

        N = self.cities.shape[0]
        dist = distance_matrix(self.cities, self.cities)

        population = self._init_population(N)
        scores = self._eval_population(population, dist)

        self.iters_without_change = 0
        self.best_idx = np.argmin(scores)
        self.stats['best_score'] = scores[self.best_idx]
        self.stats['generation_num'] = 0
        while not self._stop_condition(scores):
            self.stats['generation_num'] += 1
            self.stats['avg_score'] = np.mean(scores)
            self.stats['solution'] = population[self.best_idx]
            self.stats['iters_without_change'] = self.iters_without_change

            progress_callback.emit(self.stats)

            parents = self._select_parents(population, scores)
            pairs = self._generate_pairs(parents)
            offspring = self._procreate(parents, pairs)
            offspring = self._mutate(offspring)

            population = self._next_generation(parents, offspring)
            scores = self._eval_population(population, dist)

            
        
        return self.stats
    
    def _init_population(self, N):
        rng = np.random.default_rng()
        x = np.arange(N, dtype=np.uint16)
        perms = rng.permuted(np.tile(x, self.config.population_size).reshape(self.config.population_size, x.size), axis=1)
        return perms


    def _eval_population(self, pop, dist):
        scores = np.empty(self.config.population_size)
        rows = pop[:, :-1]
        cols = pop[:, 1:]
        for i in range(self.config.population_size):
            scores[i] = np.sum(dist[rows[i], cols[i]]) + dist[rows[i, 1], cols[i, -1]]
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
        num_of_parents = int(self.config.parents_ratio * pop.shape[0])
        probabilities = self._calculate_prob(scores)

        indices = np.random.choice(
            range(pop.shape[0]),
            size=num_of_parents,
            replace=True,
            p=probabilities
        )
        parents = pop[indices, :]

        return parents

    def _generate_pairs(self, parents):
        if self.config.include_parents:
            offspring_size = self.config.population_size - parents.shape[0]
        else:
            offspring_size = self.config.population_size

        pairs = np.ndarray(shape=(offspring_size//2, 2), dtype=np.uint16)

        # TODO: remove loop
        for i in range(pairs.shape[0]):
            pairs[i, :] = random_pair(parents.shape[0])

        return pairs


    def _crossover(self, p1, p2):
        end = self.cities.shape[0] - 1
        
        u, v = random_pair(end)

        if v < u:
            u, v = v, u
        if v - u < 2:
            v = min(v + 1, end)
            u = max(u - 1, 0)

        o1 = np.zeros(self.cities.shape[0], dtype=np.uint16)
        o2 = np.zeros(self.cities.shape[0], dtype=np.uint16)

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
            u, v = random_pair(x.shape[0])
            x[u], x[v] = x[v], x[u]
            return x

        def mutate_offsprings(offsprings):
            return np.apply_along_axis(mutate_individual, 1, offsprings)

        is_mutated = np.array(np.random.rand(pop.shape[0]) <= self.config.mutation_prob)
        if np.any(is_mutated):
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
        if self.config.include_parents:
            return np.vstack((parents, offspring))
        else:
            return offspring

    def _stop_condition(self, scores):
        if self.is_stopped:
            return True

        self.best_idx = np.argmin(scores)
        curr_best_score = scores[self.best_idx]

        if curr_best_score < self.stats['best_score']:
            self.stats['best_score'] = curr_best_score
            self.iters_without_change = 0
            return False
        else:
            self.iters_without_change += 1
            return self.iters_without_change == self.config.max_iter