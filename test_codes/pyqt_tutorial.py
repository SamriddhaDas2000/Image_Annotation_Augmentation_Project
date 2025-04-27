from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(100, 100, 300, 300)
    win.setWindowTitle("Example")

    label = QtWidgets.QLabel(win)
    label.setText("my first label!!")
    label.move(50,50)

    win.show()
    sys.exit(app.exec_())

window()
