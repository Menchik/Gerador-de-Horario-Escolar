from tkinter import Widget
from PyQt6.QtWidgets import (
    QMainWindow,QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QFormLayout,
    QLineEdit, QLabel, QSpinBox, QPushButton, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class TeachersWindow(QWidget):
    def __init__(self, size):
        super().__init__()

        self.setWindowTitle("Professores")

        self.setMinimumSize(size)

        layout = QFormLayout()

        tab = QTabWidget()
        for color,name in [("red", "Mauro"), ("green", "Pedro"), ("blue", "Bianca"), ("yellow", "Geraldo")]:
            tab.addTab(Color(color), name)

        layout.addWidget(tab)
        self.setLayout(layout)

class GradesWindow(QWidget):
    def __init__(self, size):
        super().__init__()

        self.setWindowTitle("Turmas")

        self.setMinimumSize(size)

        layout = QFormLayout()

        tab = QTabWidget()
        for color,name in [("purple", "Quinto"), ("black", "Sexto"), ("orange", "Sétimo")]:
            tab.addTab(Color(color), name)

        layout.addWidget(tab)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.setWindowTitle("Criador de Horários")

        self.setMinimumSize(800, 450)

        button_teachers = QPushButton("Professores")
        button_teachers.clicked.connect(self.show_teachers_window)

        button_grades = QPushButton("Turmas")
        button_grades.clicked.connect(self.show_grades_window)

        layout.addWidget(button_teachers)
        layout.addWidget(button_grades)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_teachers_window(self):
        self.w = TeachersWindow(self.size())
        self.w.show()
    
    def show_grades_window(self):
        self.w = GradesWindow(self.size())
        self.w.show()

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)