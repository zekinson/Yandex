import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Gallows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def paintEvent(self, e):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Gallows()
    window.show()
    sys.exit(app.exec_())
