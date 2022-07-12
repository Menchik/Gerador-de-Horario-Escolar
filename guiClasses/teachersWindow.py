from PyQt6.QtWidgets import QTabWidget, QFormLayout, QWidget

class TeachersWindow(QWidget):
    def __init__(self, size):
        super().__init__()

        self.setWindowTitle("Professores")

        self.setMinimumSize(size)

        layout = QFormLayout()

        tab = QTabWidget()
        for color,name in [("red", "Mauro"), ("green", "Pedro"), ("blue", "Bianca"), ("yellow", "Geraldo")]:
            tab.addTab(QWidget(self), name)

        layout.addWidget(tab)
        self.setLayout(layout)