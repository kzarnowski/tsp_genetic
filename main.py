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


if __name__ == '__main__':
    cities = generate_cities()
    N = cities.shape[0]
    dist = distance_matrix(cities, cities)


    for i in range(N-1):
        plt.plot(cities[i:i+2, 0], cities[i:i+2, 1], 'ro-')
    plt.show()
