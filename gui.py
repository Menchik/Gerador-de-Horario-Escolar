from PyQt6.QtWidgets import (
    QApplication
)
from guiClasses.mainWindow import MainWindow

def openGUI():
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()

if __name__ == "__main__":
    print("This file can't be executed on its own, try main.py")