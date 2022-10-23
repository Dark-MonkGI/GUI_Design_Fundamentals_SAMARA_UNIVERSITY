from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Laboratory Work №2")
        self.setGeometry(550, 250, 400, 250)

        self.push_button = QtWidgets.QPushButton(self)
        self.push_button.move(155, 130)
        self.push_button.setText("Push Me")
        self.push_button.setFixedWidth(100)
        self.push_button.clicked.connect(self.bt_push)

        self.display_label = QtWidgets.QLabel(self)
        self.display_label.setText("This fist text")
        self.display_label.move(170, 80)
        self.display_label.adjustSize()

    def bt_push(self):
        self.display_label.setText("And this is the new text")
        self.display_label.move(150, 80)
        self.display_label.adjustSize()

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    application()


