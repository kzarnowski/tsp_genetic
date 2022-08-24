from re import S
from PyQt5.QtWidgets import (QFileDialog, QInputDialog, QWidget, QMainWindow, QHBoxLayout, 
    QVBoxLayout, QApplication, QLabel, QPushButton, QLineEdit, QSlider, QCheckBox, QMessageBox,
    QProgressBar)
from PyQt5.QtCore import QSize, Qt, QPointF, QThreadPool
from PyQt5.QtGui import QPalette, QColor, QPainter, QPixmap, QPen, QFont, QIntValidator

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

        self.threadpool = QThreadPool()
        with open('help.txt', 'r') as file:
            self.help_message = file.read()

        self.setFixedSize(QSize(*WINDOW_SIZE))
        self.setWindowTitle("Problem komiwojazera - algorytm genetyczny")

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
        self.help = QPushButton("Kliknij aby uzyskać pomoc")
        self.help.clicked.connect(self.display_help)
        self.sidebar.addWidget(self.help)
        self.sidebar.addLayout(self.settings, 7)

        self.stats = QVBoxLayout()
        self.sidebar.addLayout(self.stats, 3)

        header_font = QFont()
        header_font.setPointSize(18)
        
        # LOADING DATA
        self.data_label = QLabel("DANE")
        self.data_label.setFont(header_font)
        self.data_label.setAlignment(Qt.AlignCenter)
        self.data_label.setContentsMargins(0, 0, 0, 5)
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
        self.configuration_label = QLabel("OPCJE")
        self.configuration_label.setFont(header_font)
        self.configuration_label.setAlignment(Qt.AlignCenter)
        self.configuration_label.setContentsMargins(0, 10, 0, 5)
        self.population_size_label = QLabel("Rozmiar populacji")
        self.population_size_input = QLineEdit()
        self.population_size_input.setValidator(QIntValidator())
        
        self.settings.addWidget(self.configuration_label)
        self.settings.addWidget(self.population_size_label)
        self.settings.addWidget(self.population_size_input)

        """
        Setup parents ratio layout.
        """
        self.parents_ratio_label = QLabel("Wybór rodziców:")
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
        self.mutation_prob_label = QLabel("Prawdopodobieństwo mutacji:")
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

        # MAX ITERS WITHOUT CHANGE
        self.max_iter_label = QLabel("Dociekliwość:")
        self.max_iter_layout = QHBoxLayout()
        self.max_iter_layout.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
        self.max_iter_slider = QSlider()
        self.max_iter_slider.setMinimum(30)
        self.max_iter_slider.setMaximum(500)
        self.max_iter_slider.setOrientation(Qt.Horizontal)
        self.max_iter_display = QLabel()
        self.max_iter_slider.valueChanged.connect(lambda: {
            self.max_iter_display.setText(
                "Bardzo niska" if self.max_iter_slider.value() < 100 else
                "Niska" if self.max_iter_slider.value() < 200 else
                "Średnia" if self.max_iter_slider.value() < 300 else
                "Wysoka" if self.max_iter_slider.value() < 400 else
                "Bardzo wysoka"
            )
        })

        self.settings.addWidget(self.max_iter_label)
        self.settings.addLayout(self.max_iter_layout)
        self.max_iter_layout.addWidget(self.max_iter_slider, 2)
        self.max_iter_layout.addWidget(self.max_iter_display, 1)

        # INCLUDE PARENTS
        self.include_parents_checkbox = QCheckBox()
        self.include_parents_checkbox.setChecked(True)
        self.include_parents_checkbox.setText("Przekazuj rodziców")
        self.settings.addWidget(self.include_parents_checkbox)

        # START/STOP BUTTON
        self.start_stop_button = QPushButton()
        # self.start_stop_button.setFixedHeight(40)
        self.start_stop_button.setText("START")
        self.settings.addWidget(self.start_stop_button)

        # STATS
        self.stats_label = QLabel("STATYSTYKI")
        self.stats_label.setFont(header_font)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats.addWidget(self.stats_label)
        self.generation_num = QLabel("Pokolenie:")
        self.stats.addWidget(self.generation_num)
        self.top_score = QLabel("Najlepszy wynik:")
        self.stats.addWidget(self.top_score)
        self.avg_score = QLabel("Średni wynik:")
        self.stats.addWidget(self.avg_score)

        # PROGRESS BAR
        self.progressbar_label = QLabel("Pozostały czas:")
        self.stats.addWidget(self.progressbar_label)
        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(False)
        self.progressbar.setInvertedAppearance(True)
        self.style_progressbar()
        self.stats.addWidget(self.progressbar)

        # HELPERS
        self.settings_widgets = [
            self.data_label,
            self.load_data_button,
            self.generate_random_button,
            self.configuration_label,
            self.population_size_input,
            self.population_size_label,
            self.parents_ratio_label,
            self.parents_ratio_display,
            self.parents_ratio_slider,
            self.mutation_prob_slider,
            self.mutation_prob_display,
            self.mutation_prob_label,
            self.max_iter_label,
            self.max_iter_slider,
            self.max_iter_display,
            self.include_parents_checkbox
        ]

        self.stats_widgets = [
            self.stats_label,
            self.generation_num,
            self.top_score,
            self.avg_score,
            self.progressbar,
            self.progressbar_label
        ]

    def display_help(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setBaseSize(700, 700)
        box.setInformativeText(self.help_message)
        box.exec()

    def display_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Text files (*.txt)")

        if dialog.exec_():
            filenames = dialog.selectedFiles()    
            self.app.set_cities_from_txt(filenames[0])

    def display_warning(self, message):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setText(message)
        box.exec()
    
    def display_cities_count_dialog(self):
        num_of_cities, ok = QInputDialog.getInt(
            None,
            "Random mode: number of cities",
            "Enter a number of cities"
        )
        
        if num_of_cities < 3:
            self.display_warning("Minimalna liczba miast: 3")
            return

        if ok:
            self.app.set_cities_random(num_of_cities)
    
    def setup_default_config(self, config):
        self.mutation_prob_display.setText(f"{config.mutation_prob} %")
        self.mutation_prob_slider.setValue(flt2per(config.mutation_prob))
        self.parents_ratio_display.setText(f"{config.parents_ratio} %") 
        self.parents_ratio_slider.setValue(flt2per(config.parents_ratio))
        self.population_size_input.setText(str(config.population_size))
        self.max_iter_slider.setValue(config.max_iter)
        self.start_stop_button.clicked.connect(self.app.start_stop_clicked)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(config.max_iter-1)
        self.after()

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

    def update_stats(self, curr_stats):
        self.generation_num.setText(f"Pokolenie: {curr_stats['generation_num']}")
        self.top_score.setText(f"Najlepszy wynik: {round(curr_stats['best_score'], 3)}")
        self.avg_score.setText(f"Średni wynik: {round(curr_stats['avg_score'], 3)}")
        self.progressbar.setValue(curr_stats["iters_without_change"])
        self.style_progressbar()
        
    
    def style_progressbar(self):
        if self.progressbar.value() == -1:
            red, green, blue = 0, 0, 0
        else:
            progress_percent = ((self.progressbar.value() - self.progressbar.minimum()) / 
                (self.progressbar.maximum() - self.progressbar.minimum()))
            red = 255 * progress_percent
            green = 255 - red
            blue = 0

        self.progressbar.setStyleSheet("""
        QProgressBar{
            border: 2px solid grey;"""
            f"background-color: rgb({red},{green},{blue});"
            "border-radius: 30%;"
        """}
        QProgressBar::chunk {
            background-color: black;
            border-radius: 30%;
        }"""
        )
    
    def draw_paths(self, curr_stats):
        painter = QPainter(self.canvas.pixmap())
        pen = QPen()
        pen.setWidth(1)

        if self.best_score is None or self.best_score > curr_stats['best_score']:
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
        self.progressbar.setMaximum(self.app.config.max_iter-1)

    def closeEvent(self, event):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Zamykanie programu')
        if self.app.ga.is_stopped:
            box.setText('Czy na pewno chcesz zakończyć program?')
        else:
            box.setText('Symulacja w trakcie! Czy na pewno chcesz zakończyć program?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = box.button(QMessageBox.Yes)
        btn_yes.setText('Zamknij')
        btn_no = box.button(QMessageBox.No)
        btn_no.setText('Anuluj')
        box.exec_()

        if box.clickedButton() == btn_yes:
            self.app.ga.is_stopped = True
            event.accept()
        elif box.clickedButton() == btn_no:
            event.ignore()
    
    def before(self):
        for widget in self.settings_widgets:
            widget.setEnabled(False)
        for widget in self.stats_widgets:
            widget.setEnabled(True)
        self.start_stop_button.setText("STOP")

    def after(self):
        for widget in self.settings_widgets:
            widget.setEnabled(True)
        for widget in self.stats_widgets:
            widget.setEnabled(False)
        self.start_stop_button.setText("START")
        self.progressbar.setValue(self.progressbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

