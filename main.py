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
    x = np.arange(N)
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


if __name__ == '__main__':
    cities = generate_cities()
    N = cities.shape[0]
    dist = distance_matrix(cities, cities)

    population = init_population()
    scores = eval_population(population)

    parents = select_parents(population, scores)

    print(parents)
    # for i in range(N-1):
    #     plt.plot(cities[i:i+2, 0], cities[i:i+2, 1], 'ro-')
    # plt.show()
