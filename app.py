import numpy as np
from algo import GeneticAlgorithm
from config import Config
from utils import per2flt
from workers import Worker

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
        self.ui.reset_canvas()
        self.ui.draw_cities(cities)

    def set_cities_from_txt(self, path):
        try:
            cities = np.loadtxt(path)
        except:
            self.ui.display_warning("Wystąpił błąd. Plik ma nieprawidłową" 
                " strukturę lub jest uszkodzony.")
            return

        if cities.shape[1] != 2:
            self.ui.display_warning("Wybrany plik ma nieprawidłową strukturę.")
            return

        self.ga.set_cities(cities)
        self.ui.reset_canvas()
        self.ui.draw_cities(cities)

    def update_config(self):
        params = {}
        params["population_size"] = int(self.ui.population_size_input.text())
        params["mutation_prob"] = per2flt(self.ui.mutation_prob_slider.value())
        params["parents_ratio"] = per2flt(self.ui.parents_ratio_slider.value())
        params["include_parents"] = self.ui.include_parents_checkbox.isChecked()
        params["max_iter"] = self.ui.max_iter_slider.value()
        self.config.update(params)

    def start_stop_clicked(self):
        if self.ui.px is None or self.ui.py is None:
            self.ui.display_warning("Załaduj dane przed uruchomieniem algorytmu.")
            return
        
        if int(self.ui.population_size_input.text()) < 100:
            self.ui.display_warning("W celu skutecznego działania algorytmu minimalna"
            " liczba osobników wynosi 100")
            return

        if self.ga.is_stopped:
            self.run_ga()   
        else:
            self.complete()
    
    def progress(self, stats):
        """ Przekazuje do ui aktualny wynik"""
        self.ui.update_stats(stats)
        self.ui.draw_paths(stats)
        self.ui.draw_cities(self.ga.cities)

    def result(self, stats):
        """ Wynik algorytmu po zatrzymaniu """
        self.ui.draw_paths(stats)

    def complete(self):
        """ Wywołuje się po zatrzymaniu algorytmu """
        self.ga.is_stopped = True
        self.ui.after()
    
    def run_ga(self):
        """ Uruchamia algorytm """
        self.update_config()
        self.ui.reset_canvas()
        self.ui.draw_cities(self.ga.cities)
        self.worker = Worker(self.ga.run_algorithm)
        self.worker.signals.result.connect(self.result)
        self.worker.signals.finished.connect(self.complete)
        self.worker.signals.progress.connect(self.progress)
        self.ga.is_stopped = False
        self.ui.before()
        self.ui.threadpool.start(self.worker)