from PyQt5.QtWidgets import QApplication
from window import MainWindow

app = QApplication([])

window = MainWindow(True)
window.show()

app.exec()
