from PyQt6.QtWidgets import (
    QMainWindow,QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QFormLayout,
    QLineEdit, QLabel, QSpinBox, QPushButton, QTabWidget, QToolBar, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from guiClasses.teachersWindow import TeachersWindow
from guiClasses.gradesWindow import GradesWindow
from guiClasses.warning import CustomDialog



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.tw = None
        self.gw = None

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

        toolbar = QToolBar("Teste")
        self.addToolBar(toolbar)

        button_action = QAction("Button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyButtonClick)
        toolbar.addAction(button_action)

    def onMyButtonClick(self, s):
        print("click", s)
        dlg = CustomDialog(self)
        if  dlg.exec():
            print("Cool")
        else:
            print("Shit")

    def show_teachers_window(self):
        if self.tw is None:
            self.tw = TeachersWindow(self.size())
            self.tw.show()
        else:
            print("Already opened")
    
    def show_grades_window(self):
        if self.gw is None:
            self.gw = GradesWindow(self.size())
            self.gw.show()
        else:
            print("Already opened")