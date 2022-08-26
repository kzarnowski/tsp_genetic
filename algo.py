import numpy as np
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

        # Inicjalizacja i ocena populacji początkowej
        population = self.init_population(self.cities.shape[0])
        dist = distance_matrix(self.cities, self.cities)
        scores = self.eval_population(population, dist)
        self.iters_without_change = 0
        self.best_idx = np.argmin(scores)
        self.stats['best_score'] = scores[self.best_idx]
        self.stats['generation_num'] = 0

        # Szukanie rozwiązania
        while not self.stop_condition(scores):
            # aktualizacja statystyk
            self.stats['generation_num'] += 1
            self.stats['avg_score'] = np.mean(scores)
            self.stats['solution'] = population[self.best_idx]
            self.stats['iters_without_change'] = self.iters_without_change
            # wysłanie biezacych wyników
            progress_callback.emit(self.stats) 

            # ALGORYTM:

            # 1. Wybranie rodziców którzy będą brać udział w krzyzowaniu
            parents = self.select_parents(population, scores)
            # 2. Utworzenie odpowiedniej liczby par, tak aby zachować rozmiar populacji
            pairs = self.generate_pairs(parents)
            # 3. Utworzenie osobników potomnych poprzez krzyzowanie
            offspring = self.procreate(parents, pairs)
            # 4. Mutacja osobników potomnych
            offspring = self.mutate(offspring)
            # 5. Utworzenie następnego pokolenia
            population = self.next_generation(parents, offspring)
            # 6. Ocena nowo utworzonej populacji
            scores = self.eval_population(population, dist)       
        
        return self.stats
    
    def init_population(self, N):
        """ Generuje N losowych rozwiązań """
        rng = np.random.default_rng()
        x = np.arange(N, dtype=np.uint16)
        perms = rng.permuted(np.tile(x, self.config.population_size) \
        .reshape(self.config.population_size, x.size), axis=1)
        return perms

    def eval_population(self, pop, dist):
        """ Obliczenie długości ściezek """
        scores = np.empty(self.config.population_size)
        rows = pop[:, :-1]
        cols = pop[:, 1:]
        for i in range(self.config.population_size):
            scores[i] = np.sum(dist[rows[i], cols[i]]) + dist[rows[i, 1], cols[i, -1]]
        return scores

    def calculate_prob(self, scores):
        """ Autorska metoda obliczania prawdopodobieństwa do metody ruletki """
        total_cost = np.sum(scores)
        inv_ratio = total_cost / scores
        total_inv_ratio = np.sum(inv_ratio)
        return inv_ratio / total_inv_ratio

    def select_parents(self, pop, scores):
        """
        Wybór rodziców do rozmnazania metodą ruletki z odwróconym prawdopodobieństwem,
        z uwagi na fakt ze szukamy osobników z najmniejszym stosunkiem długości ściezki 
        do sumy sciezek wszystkich osobników.
        """
        num_of_parents = int(self.config.parents_ratio * pop.shape[0])
        probabilities = self.calculate_prob(scores)
        indices = np.random.choice(
            range(pop.shape[0]),
            size=num_of_parents,
            replace=True,
            p=probabilities
        )
        parents = pop[indices, :]
        return parents

    def generate_pairs(self, parents):
        if self.config.include_parents:
            offspring_size = self.config.population_size - parents.shape[0]
        else:
            offspring_size = self.config.population_size
        pairs = np.ndarray(shape=(offspring_size//2, 2), dtype=np.uint16)
        for i in range(pairs.shape[0]):
            pairs[i, :] = random_pair(parents.shape[0])
        return pairs

    def crossover(self, p1, p2):
        """
        Opis operacji krzyzowania na podstawie ktorego powstala moja implementacja:
        https://www.hindawi.com/journals/cin/2017/7430125/
        """
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

    def mutate(self, pop):
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

    def procreate(self, parents, pairs):
        offspring = np.ndarray(shape=(
            2*pairs.shape[0],
            parents.shape[1]
        ), dtype=np.uint16)

        i = 0
        while i < 2*pairs.shape[0]:
            p1 = parents[pairs[i//2, 0], :]
            p2 = parents[pairs[i//2, 1], :]
            o1, o2 = self.crossover(p1, p2)
            offspring[i, :] = o1
            offspring[i+1, :] = o2
            i += 2
        return offspring

    def next_generation(self, parents, offspring):
        if self.config.include_parents:
            return np.vstack((parents, offspring))
        else:
            return offspring

    def stop_condition(self, scores):
        if self.is_stopped:
            # Algorytm został zatrzymany przez UI
            return True

        self.best_idx = np.argmin(scores)
        curr_best_score = scores[self.best_idx]

        if curr_best_score < self.stats['best_score']:
            # Znaleziono lepsze rozwiazanie, szukaj dalej
            self.stats['best_score'] = curr_best_score
            self.iters_without_change = 0
            return False
        else:
            self.iters_without_change += 1
            # Brak lepszego rozwiazania, sprawdzamy czy osiagnieto maksymalną liczbe iteracji
            return self.iters_without_change == self.config.max_iter