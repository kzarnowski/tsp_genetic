import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from random import random

import configuration as CONFIG

# TODO: temporary
iters_without_change = None
best_idx = None
best_score = None

def generate_cities():
    if CONFIG.RANDOM_MODE:
        x = np.random.uniform(0, CONFIG.WIDTH, CONFIG.NUM_OF_CITIES)
        y = np.random.uniform(0, CONFIG.HEIGHT, CONFIG.NUM_OF_CITIES)
        cities = np.column_stack((x, y))
    else:
        cities = np.loadtxt(CONFIG.CITIES_FILEPATH)
        #TODO: check file structure
    return cities


def init_population(N):
    rng = np.random.default_rng()
    x = np.arange(N, dtype=np.uint16)
    perms = rng.permuted(np.tile(x, CONFIG.POPULATION_SIZE).reshape(CONFIG.POPULATION_SIZE, x.size), axis=1)
    return perms


def eval_population(pop, dist):
    scores = np.empty(CONFIG.POPULATION_SIZE)
    rows = pop[:, :-1]
    cols = pop[:, 1:]
    for i in range(CONFIG.POPULATION_SIZE):
        scores[i] = np.sum(dist[rows[i], cols[i]])
    return scores


def calculate_prob(scores):
    total_cost = np.sum(scores)
    inv_ratio = total_cost / scores
    total_inv_ratio = np.sum(inv_ratio)
    return inv_ratio / total_inv_ratio


def select_parents(pop, scores):
    """
    Roulette-wheel method with inversed probability.
    """
    num_of_parents = int(CONFIG.PARENTS_RATIO * pop.shape[0])
    probabilities = calculate_prob(scores)

    indices = np.random.choice(
        range(pop.shape[0]),
        size=num_of_parents,
        replace=True,
        p=probabilities
    )
    parents = pop[indices, :]

    return parents


def random_pair(max_value):
    rng = np.random.default_rng()
    idx = rng.choice(max_value, 2, replace=False)
    return idx[0], idx[1]


def generate_pairs(parents):
    if CONFIG.INCLUDE_PARENTS:
        offspring_size = CONFIG.POPULATION_SIZE - parents.shape[0]
    else:
        offspring_size = CONFIG.POPULATION_SIZE

    pairs = np.ndarray(shape=(offspring_size//2, 2), dtype=np.uint16)

    # TODO: remove loop
    for i in range(pairs.shape[0]):
        pairs[i, :] = random_pair(parents.shape[0])

    return pairs


def crossover(p1, p2):
    end = CONFIG.NUM_OF_CITIES - 1
    u, v = random_pair(end)

    if v < u:
        u, v = v, u
    if v - u < 2:
        v = min(v + 1, end)
        u = max(u - 1, 0)

    o1 = np.zeros(CONFIG.NUM_OF_CITIES, dtype=np.uint16)
    o2 = np.zeros(CONFIG.NUM_OF_CITIES, dtype=np.uint16)

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


def mutate(pop):
    def mutate_individual(x):
        u, v = random_pair(x.shape[0])
        x[u], x[v] = x[v], x[u]
        return x

    def mutate_offsprings(offsprings):
        return np.apply_along_axis(mutate_individual, 1, offsprings)

    is_mutated = np.array(np.random.rand(pop.shape[0]) <= CONFIG.MUTATION_PROBABILITY)
    pop[is_mutated] = mutate_offsprings(pop[is_mutated])
    return pop


def procreate(parents, pairs):
    offspring = np.ndarray(shape=(
        2*pairs.shape[0],
        parents.shape[1]
    ), dtype=np.uint16)

    i = 0
    while i < 2*pairs.shape[0]:
        p1 = parents[pairs[i//2, 0], :]
        p2 = parents[pairs[i//2, 1], :]
        o1, o2 = crossover(p1, p2)
        offspring[i, :] = o1
        offspring[i+1, :] = o2
        i += 2
    return offspring


def next_generation(parents, offspring):
    if CONFIG.INCLUDE_PARENTS:
        return np.vstack((parents, offspring))
    else:
        return offspring

def stop_condition(scores):
    global iters_without_change
    global best_idx
    global best_score

    curr_best_idx = np.argmin(scores)
    curr_best_score = scores[curr_best_idx]

    if curr_best_score < best_score:
        best_score = curr_best_score
        best_idx = curr_best_idx
        iters_without_change = 0
        return False
    else:
        iters_without_change += 1
        return iters_without_change == CONFIG.MAX_ITER

def run_algorithm():
    global iters_without_change
    global best_idx
    global best_score
    
    cities = generate_cities()
    N = cities.shape[0]
    dist = distance_matrix(cities, cities)

    population = init_population(N)
    scores = eval_population(population, dist)

    iters_without_change = 0
    best_idx = np.argmin(scores)
    best_score = scores[best_idx]

    gen = 0
    while not stop_condition(scores):
        if gen % 10 == 0:
            print(f"GEN: {gen} BEST: {best_score} SOLUTION: {population[best_idx]} ALL: {np.sum(scores)}")
        gen += 1

        parents = select_parents(population, scores)
        pairs = generate_pairs(parents)
        offspring = procreate(parents, pairs)

        offspring = mutate(offspring)

        population = next_generation(parents, offspring)
        scores = eval_population(population, dist)