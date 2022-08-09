from PyQt5 import QtCore, QtGui, QtWidgets
from genetic_algorithm import run_algorithm

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
        self.pop_size_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pop_size_input.setGeometry(QtCore.QRect(1000, 170, 113, 21))
        self.pop_size_input.setObjectName("pop_size_input")
        self.pop_size_label = QtWidgets.QLabel(self.centralwidget)
        self.pop_size_label.setGeometry(QtCore.QRect(860, 170, 91, 20))
        self.pop_size_label.setObjectName("pop_size_label")
        self.mutation_prob_slider = QtWidgets.QSlider(self.centralwidget)
        self.mutation_prob_slider.setGeometry(QtCore.QRect(1000, 210, 121, 22))
        self.mutation_prob_slider.setOrientation(QtCore.Qt.Horizontal)
        self.mutation_prob_slider.setObjectName("mutation_prob_slider")
        self.mutation_prob_label = QtWidgets.QLabel(self.centralwidget)
        self.mutation_prob_label.setGeometry(QtCore.QRect(850, 200, 141, 41))
        self.mutation_prob_label.setObjectName("mutation_prob_label")
        self.parents_ratio_label = QtWidgets.QLabel(self.centralwidget)
        self.parents_ratio_label.setGeometry(QtCore.QRect(870, 250, 91, 16))
        self.parents_ratio_label.setObjectName("parents_ratio_label")
        self.parents_ratio_slider = QtWidgets.QSlider(self.centralwidget)
        self.parents_ratio_slider.setGeometry(QtCore.QRect(1000, 250, 121, 22))
        self.parents_ratio_slider.setOrientation(QtCore.Qt.Horizontal)
        self.parents_ratio_slider.setObjectName("parents_ratio_slider")
        self.include_parents_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.include_parents_checkbox.setGeometry(QtCore.QRect(860, 310, 171, 20))
        self.include_parents_checkbox.setObjectName("include_parents_checkbox")
        self.start_stop_button = QtWidgets.QPushButton(self.centralwidget)

        # Controlling execution
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

        self.my_setup()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_data_button.setText(_translate("MainWindow", "Load from file"))
        self.generate_random_button.setText(_translate("MainWindow", "Generate random"))
        self.data_label.setText(_translate("MainWindow", "Data"))
        self.configuration_label.setText(_translate("MainWindow", "Configuration"))
        self.pop_size_label.setText(_translate("MainWindow", "Population size"))
        self.mutation_prob_label.setText(_translate("MainWindow", "Mutation probability"))
        self.parents_ratio_label.setText(_translate("MainWindow", "Parents ratio"))
        self.include_parents_checkbox.setText(_translate("MainWindow", "Include Parents"))
        self.start_stop_button.setText(_translate("MainWindow", "START"))

    def my_setup(self):
        self.start_stop_button.clicked.connect(run_algorithm)