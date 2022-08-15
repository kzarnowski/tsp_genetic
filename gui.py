from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from algo import GeneticAlgorithm
from config import Config
from utils import flt2per

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Basic setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 812)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Initializing data
        self.load_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_data_button.setGeometry(QtCore.QRect(870, 70, 121, 41))
        self.load_data_button.setObjectName("load_data_button")
        self.load_data_button.clicked.connect(self.display_file_dialog)

        self.generate_random_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_random_button.setGeometry(QtCore.QRect(990, 70, 141, 41))
        self.generate_random_button.setObjectName("generate_random_button")
        self.data_label = QtWidgets.QLabel(self.centralwidget)
        self.data_label.setGeometry(QtCore.QRect(970, 40, 60, 16))
        self.data_label.setObjectName("data_label")

        # Genetic algorithm configuration
        self.configuration_label = QtWidgets.QLabel(self.centralwidget)
        self.configuration_label.setGeometry(QtCore.QRect(950, 130, 91, 20))
        self.configuration_label.setObjectName("configuration_label")
        
        self.setup_population_size()
        
        self.include_parents_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.include_parents_checkbox.setGeometry(QtCore.QRect(860, 310, 171, 20))
        self.include_parents_checkbox.setObjectName("include_parents_checkbox")
        self.include_parents_checkbox.setChecked(True)
        
        self.setup_parents_ratio()
        self.setup_mutation_prob()

        # Controlling execution
        self.start_stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_stop_button.setGeometry(QtCore.QRect(930, 410, 113, 32))
        self.start_stop_button.setObjectName("start_stop_button")

        # Menu and status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_data_button.setText(_translate("MainWindow", "Load from file"))
        self.generate_random_button.setText(_translate("MainWindow", "Generate random"))
        self.data_label.setText(_translate("MainWindow", "Data"))
        self.configuration_label.setText(_translate("MainWindow", "Configuration"))
        self.population_size_label.setText(_translate("MainWindow", "Population size"))
        self.mutation_prob_label.setText(_translate("MainWindow", "Mutation probability"))
        self.parents_ratio_label.setText(_translate("MainWindow", "Parents ratio"))
        self.include_parents_checkbox.setText(_translate("MainWindow", "Include Parents"))
        self.start_stop_button.setText(_translate("MainWindow", "START"))

    def display_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Text files (*.txt)")

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            print(filenames[0])

    def setup_mutation_prob(self):
        self.mutation_prob_label = QtWidgets.QLabel(self.centralwidget)
        self.mutation_prob_label.setGeometry(QtCore.QRect(850, 200, 141, 41))
        self.mutation_prob_label.setObjectName("mutation_prob_label")

        self.mutation_prob_slider = QtWidgets.QSlider(self.centralwidget)
        self.mutation_prob_slider.setGeometry(QtCore.QRect(1000, 210, 121, 22))
        self.mutation_prob_slider.setOrientation(QtCore.Qt.Horizontal)
        self.mutation_prob_slider.setObjectName("mutation_prob_slider")
        self.mutation_prob_slider.setMinimum(0)
        self.mutation_prob_slider.setMaximum(100)

        self.mutation_prob_display = QtWidgets.QLabel(self.centralwidget)
        self.mutation_prob_display.setGeometry(QtCore.QRect(200, 200, 50, 50))
        self.mutation_prob_display.setObjectName("mutation_prob_display")

        self.mutation_prob_slider.valueChanged.connect(lambda: {
            self.mutation_prob_display.setText(
                f"{self.mutation_prob_slider.value()} %"
            )
        })
        
    def setup_parents_ratio(self):
        self.parents_ratio_label = QtWidgets.QLabel(self.centralwidget)
        self.parents_ratio_label.setGeometry(QtCore.QRect(870, 250, 91, 16))
        self.parents_ratio_label.setObjectName("parents_ratio_label")

        self.parents_ratio_slider = QtWidgets.QSlider(self.centralwidget)
        self.parents_ratio_slider.setGeometry(QtCore.QRect(1000, 250, 121, 22))
        self.parents_ratio_slider.setOrientation(QtCore.Qt.Horizontal)
        self.parents_ratio_slider.setObjectName("parents_ratio_slider")
        self.parents_ratio_slider.setMinimum(0)
        self.parents_ratio_slider.setMaximum(100)

        self.parents_ratio_display = QtWidgets.QLabel(self.centralwidget)
        self.parents_ratio_display.setGeometry(QtCore.QRect(200, 250, 50, 50))
        self.parents_ratio_display.setObjectName("parents_ratio_display")

        self.parents_ratio_slider.valueChanged.connect(lambda: {
            self.parents_ratio_display.setText(
                f"{self.parents_ratio_slider.value()} %"
            )
        })

    def setup_default_config(self, config):
        self.mutation_prob_display.setText(f"{config.mutation_prob} %")
        self.mutation_prob_slider.setValue(flt2per(config.mutation_prob))
        self.parents_ratio_display.setText(f"{config.parents_ratio} %") 
        self.parents_ratio_slider.setValue(flt2per(config.parents_ratio))
        self.population_size_input.setText(str(config.population_size))
    
    def setup_population_size(self):
        self.population_size_input = QtWidgets.QLineEdit(self.centralwidget)
        self.population_size_input.setGeometry(QtCore.QRect(1000, 170, 113, 21))
        self.population_size_input.setObjectName("pop_size_input")

        self.population_size_label = QtWidgets.QLabel(self.centralwidget)
        self.population_size_label.setGeometry(QtCore.QRect(860, 170, 91, 20))
        self.population_size_label.setObjectName("pop_size_label")

