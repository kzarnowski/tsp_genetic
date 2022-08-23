import algo
from gui2 import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from app import App

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    MainApplication = App(window)
    window.show()

    sys.exit(app.exec_())
