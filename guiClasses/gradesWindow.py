from PyQt6.QtWidgets import QTabWidget, QFormLayout, QWidget

class GradesWindow(QWidget):
    def __init__(self, size):
        super().__init__()

        self.setWindowTitle("Turmas")

        self.setMinimumSize(size)

        layout = QFormLayout()

        tab = QTabWidget()
        for color,name in [("purple", "Quinto"), ("black", "Sexto"), ("orange", "Sétimo")]:
            tab.addTab(QWidget(self), name)

        layout.addWidget(tab)
        self.setLayout(layout)