import numpy as np
from algo import GeneticAlgorithm
from config import Config
from utils import per2flt

class App():
    def __init__(self, ui):
        self.ui = ui
        self.config = Config()
        self.ui.setup_default_config(self.config)
        self.ga = GeneticAlgorithm(self.config)
        self.setup_actions()

    def get_cities_random(num_of_cities):
        x = np.random.uniform(0, 100, num_of_cities)
        y = np.random.uniform(0, 100, num_of_cities)
        return np.column_stack((x, y))

    def get_cities_from_txt(path):
        cities = np.loadtxt(path)
        #TODO: check file structure
        return cities

    def run_ga(self):
        self.ga.run_algorithm()

    def update_config(self):
        params = {}
        params["population_size"] = int(self.ui.population_size_input.text())
        params["mutation_prob"] = per2flt(self.ui.mutation_prob_slider.value())
        params["parents_ratio"] = per2flt(self.ui.parents_ratio_slider.value())
        params["include_parents"] = self.ui.include_parents_checkbox.isChecked()
        self.config.update(params)

        print(self.config)

    def setup_actions(self):
        self.ui.start_stop_button.clicked.connect(self.start_stop_clicked)

    def start_stop_clicked(self):
        self.update_config()
        self.ga.run_algorithm()