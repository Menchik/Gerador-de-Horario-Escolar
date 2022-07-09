from PyQt6.QtWidgets import (
    QMainWindow, QCheckBox
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QCheckBox("This is a checkbox")
        widget.setCheckState(Qt.CheckState.PartiallyChecked)

        # For tristate: widget.setCheckState(Qt.PartiallyChecked)
        # Or: widget.setTriState(True)
        widget.stateChanged.connect(self.show_state)
        widget.setTristate(True)

        self.setCentralWidget(widget)


    def show_state(self, s):
        print(s == Qt.CheckState.Checked)
        print(s)