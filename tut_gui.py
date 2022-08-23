from re import L
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(1000, 800))
        self.label = QLabel()
        canvas = QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        painter = QPainter(self.label.pixmap())
        painter.drawLine(10, 10, 300, 200)
        painter.end()



class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()



# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setWindowTitle("My App")
#         self.setFixedSize(QSize(400, 300))

#         self.label = QLabel()
#         self.input = QLineEdit()
#         self.input.textChanged.connect(self.label.setText)


#         layout = QVBoxLayout()
#         layout.addWidget(self.input)
#         layout.addWidget(self.label)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#     def clicked(self):
#         self.button.setText("Clicked")
#         self.button.setEnabled(False)
#         self.setWindowTitle("New title")
    
#     def title(self, window_title):
#         print("Window title has changed")
#         if window_title == "New title":
#             print("HEHE")
    
#     def mouseMoveEvent(self, e):
#         print("Mouse moved:", e)
    
#     def mousePressEvent(self, e):
#         self.label.setText(str(e.buttons()))