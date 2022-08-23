import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtCore

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.active = False

        self.button = QPushButton(self)
        self.button.setGeometry(QRect(200, 200, 50, 50))
        self.button.setText("Click me")
        self.setObjectName("btn")
        self.button.clicked.connect(self.button_clicked)

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Drawing')
        self.show()
    
    def retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
    
    def paintEvent(self, event):
        print(event)

        if self.active:
            painter = QPainter()
            painter.begin(self)
            self.draw(event, painter)
            painter.end()
    
    def draw(self, event, painter):
        painter.setPen(Qt.red)
        painter.drawRect(10, 10, 100, 100)

    def button_clicked(self):
        if self.active:
            self.active = False
        else:
            self.active = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())