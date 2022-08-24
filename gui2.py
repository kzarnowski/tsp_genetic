from re import S
from PyQt5.QtWidgets import (QFileDialog, QInputDialog, QWidget, QMainWindow, QHBoxLayout, 
    QVBoxLayout, QApplication, QLabel, QPushButton, QLineEdit, QSlider, QCheckBox, QMessageBox)
from PyQt5.QtCore import QSize, Qt, QPointF, QThreadPool
from PyQt5.QtGui import QPalette, QColor, QPainter, QPixmap, QPen

from utils import flt2per
import numpy as np

import sys

CANVAS_SIZE = (700, 700)
WINDOW_SIZE = (1020, 720)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.app = None
        self.px = None
        self.py = None
        self.best_score = None
        self.solution = None

        self.setFixedSize(QSize(*WINDOW_SIZE))
        self.setWindowTitle("Travelling Salesman Problem - Genetic Algorithm")

        self.container = QWidget()
        self.layout = QHBoxLayout()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.pixmap = QPixmap(*CANVAS_SIZE)
        self.pixmap.fill(QColor("white"))
        self.canvas = QLabel()
        self.canvas.setPixmap(self.pixmap)
        self.layout.addWidget(self.canvas, 10)

        self.sidebar = QVBoxLayout()
        self.layout.addLayout(self.sidebar, 4)


        self.settings = QVBoxLayout()
        self.sidebar.addLayout(self.settings, 3)

        self.stats = QVBoxLayout()
        self.sidebar.addLayout(self.stats, 7)


        # LOADING DATA
        self.data_label = QLabel("Dane")
        self.load_data_button = QPushButton()
        self.load_data_button.setText("Wczytaj z pliku txt")
        self.load_data_button.clicked.connect(self.display_file_dialog)
        self.generate_random_button = QPushButton()
        self.generate_random_button.setText("Losuj")
        self.generate_random_button.clicked.connect(self.display_cities_count_dialog)

        self.settings.addWidget(self.data_label)
        self.settings.addWidget(self.load_data_button)
        self.settings.addWidget(self.generate_random_button)

        # CONFIGURATION PANEL
        self.configuration_label = QLabel("Opcje")
        self.population_size_label = QLabel("Liczba osobników w populacji")
        self.population_size_input = QLineEdit()
        
        self.settings.addWidget(self.configuration_label)
        self.settings.addWidget(self.population_size_label)
        self.settings.addWidget(self.population_size_input)

        """
        Setup parents ratio layout.
        """
        self.parents_ratio_label = QLabel("Ile rodziców do rozmnażania:")
        self.parents_ratio_layout = QHBoxLayout()
        self.parents_ratio_layout.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)

        self.parents_ratio_slider = QSlider()
        self.parents_ratio_slider.setMinimum(0)
        self.parents_ratio_slider.setMaximum(100)
        self.parents_ratio_slider.setOrientation(Qt.Horizontal)
        self.parents_ratio_slider.setFixedWidth(220)

        self.parents_ratio_display = QLabel()
        self.parents_ratio_slider.valueChanged.connect(lambda: {
            self.parents_ratio_display.setText(
                f"{self.parents_ratio_slider.value()} %"
            )
        })

        self.settings.addWidget(self.parents_ratio_label)
        self.settings.addLayout(self.parents_ratio_layout)
        self.parents_ratio_layout.addWidget(self.parents_ratio_slider, 19)
        self.parents_ratio_layout.addWidget(self.parents_ratio_display, 1)

        """
        Setup mutation probability layout.
        """
        self.mutation_prob_label = QLabel("Prawdopodobieństwo mutacji")
        self.mutation_prob_layout = QHBoxLayout()
        self.mutation_prob_layout.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)

        self.mutation_prob_slider = QSlider()
        self.mutation_prob_slider.setMinimum(0)
        self.mutation_prob_slider.setMaximum(100)
        self.mutation_prob_slider.setOrientation(Qt.Horizontal)
        self.mutation_prob_slider.setFixedWidth(220)

        self.mutation_prob_display = QLabel()
        self.mutation_prob_slider.valueChanged.connect(lambda: {
            self.mutation_prob_display.setText(
                f"{self.mutation_prob_slider.value()} %"
            )
        })

        self.settings.addWidget(self.mutation_prob_label)
        self.settings.addLayout(self.mutation_prob_layout)
        self.mutation_prob_layout.addWidget(self.mutation_prob_slider, 19)
        self.mutation_prob_layout.addWidget(self.mutation_prob_display, 1)

        # INCLUDE PARENTS
        self.include_parents_checkbox = QCheckBox()
        self.include_parents_checkbox.setChecked(True)
        self.include_parents_checkbox.setText("Rodzice w następnym pokoleniu")
        self.settings.addWidget(self.include_parents_checkbox)

        # START/STOP BUTTON
        self.start_stop_button = QPushButton()
        self.start_stop_button.setText("START")
        self.settings.addWidget(self.start_stop_button)

        # STATS
        self.stats_label = QLabel("Statystyki (kliknij start aby zobaczyć)")
        self.stats.addWidget(self.stats_label)
        self.generation_num = QLabel()
        self.stats.addWidget(self.generation_num)
        # self.execution_time = QLabel()
        # self.stats.addWidget(self.execution_time)
        self.top_score = QLabel()
        self.stats.addWidget(self.top_score)
        self.avg_score = QLabel()
        self.stats.addWidget(self.avg_score)


    def display_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Text files (*.txt)")

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            if len(filenames) != 1:
                pass #TODO: not one file exception
    
            self.app.set_cities_from_txt(filenames[0]) 
    
    def display_cities_count_dialog(self):
        num_of_cities, ok = QInputDialog.getInt(
            None,
            "Random mode: number of cities",
            "Enter a number of cities"
        )

        if ok:
            self.app.set_cities_random(num_of_cities)
    
    def setup_default_config(self, config):
        self.mutation_prob_display.setText(f"{config.mutation_prob} %")
        self.mutation_prob_slider.setValue(flt2per(config.mutation_prob))
        self.parents_ratio_display.setText(f"{config.parents_ratio} %") 
        self.parents_ratio_slider.setValue(flt2per(config.parents_ratio))
        self.population_size_input.setText(str(config.population_size))
        self.start_stop_button.clicked.connect(self.app.start_stop_clicked)

    def draw_cities(self, cities):
        painter = QPainter(self.canvas.pixmap())
        pen = QPen()
        pen.setWidth(5)
        painter.setPen(pen)
    
        # CLEAR OLD POINTS
        if self.px is not None or self.py is not None:
            pen.setColor(QColor("white"))
            painter.setPen(pen)
            for i in range(self.px.size):
                painter.drawPoint(self.px[i], self.py[i])

        x = cities[:, 0]
        y = cities[:, 1]

        x = CANVAS_SIZE[0] * (x - np.min(x)) / (np.max(x) - np.min(x))
        y = CANVAS_SIZE[1] * (y - np.min(y)) / (np.max(y) - np.min(y))
        margin = 20 #px
        scale_x = (CANVAS_SIZE[0] - 2 * margin) / (np.max(x) - np.min(x))
        scale_y = (CANVAS_SIZE[1] - 2 * margin) / (np.max(y) - np.min(y))
        self.px = scale_x * x + margin - np.min(x) * scale_x
        self.py = scale_y * y + margin - np.min(y) * scale_y

        pen.setColor(QColor("red")) 
        painter.setPen(pen) 
        for i in range(self.px.size):
                painter.drawPoint(self.px[i], self.py[i])
        painter.end()
        self.update()
    
    def display_no_cities_message(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setText("Załaduj dane przed uruchomieniem algorytmu.")
        box.exec()

    def update_stats(self, curr_stats):
        self.stats_label.setText("Statystyki")
        self.generation_num.setText(f"Pokolenie: {curr_stats['generation_num']}")
        self.top_score.setText(f"Najlepszy wynik: {curr_stats['best_score']}")
        self.avg_score.setText(f"Średni wynik: {curr_stats['avg_score']}")
    
    def draw_paths(self, curr_stats):
        painter = QPainter(self.canvas.pixmap())
        pen = QPen()
        pen.setWidth(1)

        if self.best_score is None or self.best_score > curr_stats['best_score']:
            print(" I SHOULD DRAW")
            self.best_score = curr_stats['best_score']
            cities_count = len(self.px)

            # CLEAR OLD PATH
            if self.solution is not None:
                pen.setColor(QColor("white"))
                painter.setPen(pen)
                
                for i in range(cities_count):
                    j = i + 1 if i != cities_count - 1 else 0

                    p1 = self.solution[i]
                    p2 = self.solution[j]

                    painter.drawLine(
                        self.px[p1], self.py[p1],
                        self.px[p2], self.py[p2]
                    )

            self.solution = curr_stats['solution']

            # DRAW NEW PATH
            pen.setColor(QColor("blue"))
            painter.setPen(pen)

            for i in range(cities_count):
                j = i + 1 if i != cities_count - 1 else 0

                p1 = self.solution[i]
                p2 = self.solution[j]

                painter.drawLine(
                    self.px[p1], self.py[p1],
                    self.px[p2], self.py[p2]
                )
        
        painter.end()
        self.update()

    def reset_canvas(self):
        self.best_score = None
        self.solution = None
        self.pixmap = QPixmap(*CANVAS_SIZE)
        self.pixmap.fill(QColor("white"))
        self.canvas.setPixmap(self.pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

