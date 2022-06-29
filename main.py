import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

import configuration as CONFIG


def generate_cities():
    if CONFIG.RANDOM_MODE:
        x = np.random.uniform(0, CONFIG.WIDTH, CONFIG.NUM_OF_CITIES)
        y = np.random.uniform(0, CONFIG.HEIGHT, CONFIG.NUM_OF_CITIES)
        cities = np.column_stack((x, y))
    else:
        cities = np.loadtxt(CONFIG.CITIES_FILEPATH)
        #TODO: check file structure
    return cities


def init_population():
    rng = np.random.default_rng(1234)
    x = np.arange(N, dtype=np.uint16)
    perms = rng.permuted(np.tile(x, CONFIG.POPULATION_SIZE).reshape(CONFIG.POPULATION_SIZE, x.size), axis=1)
    return perms


def eval_population(pop):
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


def crossover(p1, p2):
    end = CONFIG.NUM_OF_CITIES - 1
    rng = np.random.default_rng()
    indices = rng.choice(end, 2, replace=False)
    u, v = indices[0], indices[1]
    if v < u:
        u, v = v, u
    if v - u < 2:
        v = max(v - 1, 0)
        u = min(u + 1, end)
    o1 = np.zeros(CONFIG.NUM_OF_CITIES, dtype=np.uint16)
    o2 = np.zeros(CONFIG.NUM_OF_CITIES, dtype=np.uint16)

    o1[u:v+1] = p1[u:v+1]
    o2[u:v+1] = p2[u:v+1]

    p1_rest = np.roll(p1, -v)
    p2_rest = np.roll(p2, -v)

    o1_fill = np.setdiff1d(p2_rest, o1[u:v+1])
    o2_fill = np.setdiff1d(p1_rest, o2[u:v+1])

    if v != end:
        o1[v+1:end+1] = o1_fill[:end-v]
        o2[v+1:end+1] = o2_fill[:end-v]

    if u != 0:
        o1[:u] = o1_fill[end-v:]
        o2[:u] = o2_fill[end-v:]

    return o1, o2




if __name__ == '__main__':
    cities = generate_cities()
    N = cities.shape[0]
    dist = distance_matrix(cities, cities)

    population = init_population()
    scores = eval_population(population)

    parents = select_parents(population, scores)

    offspring = crossover(population[0], population[1])

    print("PARENTS:\n", population[0], population[1])
    print("\nOFFSPRING\n", offspring[0], offspring[1])

    # for i in range(N-1):
    #     plt.plot(cities[i:i+2, 0], cities[i:i+2, 1], 'ro-')
    # plt.show()
