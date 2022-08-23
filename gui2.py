from PyQt5.QtWidgets import (QFileDialog, QInputDialog, QWidget, QMainWindow, QHBoxLayout, 
    QVBoxLayout, QApplication, QLabel, QPushButton, QLineEdit, QSlider, QCheckBox)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QColor, QPainter, QPixmap, QPen

from utils import flt2per

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.app = None
        self.setFixedSize(QSize(1020, 720))
        self.setWindowTitle("Travelling Salesman Problem - Genetic Algorithm")

        self.container = QWidget()
        self.layout = QHBoxLayout()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.canvas = QLabel()
        self.canvas.setPixmap(QPixmap(700, 700))
        self.layout.addWidget(self.canvas, 10)
        

        self.sidebar = QVBoxLayout()
        self.layout.addLayout(self.sidebar, 4)


        self.settings = QVBoxLayout()
        self.sidebar.addLayout(self.settings, 3)

        self.stats = QLabel("Stats")
        self.sidebar.addWidget(self.stats, 7)


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
        self.start_stop_button.setText("Start")
        self.settings.addWidget(self.start_stop_button)

        # DRAWING TEST
        self.draw()

    def draw(self):
        painter = QPainter(self.canvas.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("red"))
        painter.setPen(pen)
        painter.drawLine(0, 0, 700, 700)
        painter.end()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

