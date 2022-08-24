import numpy as np
from algo import GeneticAlgorithm
from config import Config
from utils import per2flt
from workers import Worker

from PyQt5.QtCore import QThreadPool

class App():
    def __init__(self, ui):
        self.ui = ui
        self.config = Config()
        self.ui.app = self
        self.ui.setup_default_config(self.config)
        self.ga = GeneticAlgorithm(self.config)
        self.threadpool = QThreadPool()

    def set_cities_random(self, num_of_cities):
        x = np.random.uniform(0, 100, num_of_cities)
        y = np.random.uniform(0, 100, num_of_cities)
        cities = np.column_stack((x, y))
        self.ga.set_cities(cities)
        self.ui.reset_canvas()
        self.ui.draw_cities(cities)
        print(num_of_cities)

    def set_cities_from_txt(self, path):
        cities = np.loadtxt(path)
        #TODO: check file structure
        self.ga.set_cities(cities)
        self.ui.reset_canvas()
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

    def start_stop_clicked(self):
        if self.ui.px is None or self.ui.py is None:
            self.ui.display_no_cities_message()
            return

        if self.ga.is_stopped:
            self.update_config()
            self.ui.reset_canvas()
            self.ui.draw_cities(self.ga.cities)
            self.worker = Worker(self.ga.run_algorithm)
            self.worker.signals.result.connect(self.result)
            self.worker.signals.finished.connect(self.complete)
            self.worker.signals.progress.connect(self.progress)
            self.ga.is_stopped = False
            self.ui.start_stop_button.setText("STOP")
            self.threadpool.start(self.worker)
        else:
            self.ga.is_stopped = True
            self.ui.start_stop_button.setText("START")
    
    def progress(self, stats):
        self.ui.update_stats(stats)
        self.ui.draw_paths(stats)
        self.ui.draw_cities(self.ga.cities)

    def result(self, stats):
        self.ui.draw_paths(stats)

    def complete(self):
        print("THREAD COMPLETE!")
        