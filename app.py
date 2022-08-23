import numpy as np
from algo import GeneticAlgorithm
from config import Config
from utils import per2flt

class App():
    def __init__(self, ui):
        self.ui = ui
        self.config = Config()
        self.ui.app = self
        self.ui.setup_default_config(self.config)
        self.ga = GeneticAlgorithm(self.config)

    def set_cities_random(self, num_of_cities):
        x = np.random.uniform(0, 100, num_of_cities)
        y = np.random.uniform(0, 100, num_of_cities)
        cities = np.column_stack((x, y))
        self.ga.set_cities(cities)
        self.ui.draw_cities(cities)
        print(num_of_cities)

    def set_cities_from_txt(self, path):
        cities = np.loadtxt(path)
        #TODO: check file structure
        self.ga.set_cities(cities)
        self.ui.draw_cities(cities)
        print(f"Cities set from: {path}")

    def run_ga(self):
        self.ga.run_algorithm()

    def update_config(self):
        params = {}
        params["population_size"] = int(self.ui.population_size_input.text())
        params["mutation_prob"] = per2flt(self.ui.mutation_prob_slider.value())
        params["parents_ratio"] = per2flt(self.ui.parents_ratio_slider.value())
        params["include_parents"] = self.ui.include_parents_checkbox.isChecked()
        self.config.update(params)

        #print(self.config)

    def start_stop_clicked(self):
        self.update_config()
        self.ga.run_algorithm()