from PyQt5.QtWidgets import QApplication
from window import MainWindow

app = QApplication([])

window = MainWindow()
window.showMaximized()

app.exec()
