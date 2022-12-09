from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.exchange_rate = 0.016
        self.barrel_of_oil_price = 80.1

        self.oil = 1

        self.usd = round(self.oil * self.barrel_of_oil_price, 2)
        self.rub = round(self.usd / self.exchange_rate, 2)



        self.rubChange = ChangeRub()
        self.usdChange = ChangeUsd()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(484, 386)
        MainWindow.setTabletTracking(False)
        MainWindow.setStyleSheet("background-color: rgb(233, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(160, 310, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.pushButton_1.setObjectName("pushButton_1")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(80, 50, 70, 50))
        self.label_1.setMaximumSize(QtCore.QSize(155555, 16777215))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("background-color: rgb(255, 240, 234);")
        self.label_1.setObjectName("label_1")

        self.textEdit_1 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_1.setGeometry(QtCore.QRect(240, 50, 170, 50))
        self.textEdit_1.setStyleSheet("background-color: rgb(220, 255, 230);")
        self.textEdit_1.setObjectName("textEdit_1")
        self.textEdit_1.setText(str(self.rub))
        self.textEdit_1.setReadOnly(True)



        # self.textEdit_2 = QLineEdit(self)
        # ddd = self.textEdit_1.text



        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 140, 70, 50))
        self.label_2.setMaximumSize(QtCore.QSize(155555, 16777215))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(255, 240, 234);")
        self.label_2.setObjectName("label_2")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(240, 140, 170, 50))
        self.textEdit_2.setStyleSheet("background-color: rgb(220, 255, 230);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setText(str(self.usd))
        self.textEdit_2.setReadOnly(True)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 230, 70, 50))
        self.label_3.setMaximumSize(QtCore.QSize(155555, 16777215))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(255, 240, 234);")
        self.label_3.setObjectName("label_3")

        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(240, 230, 170, 50))
        self.textEdit_3.setStyleSheet("background-color: rgb(220, 255, 230);")
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setText(str(self.oil))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.rubChange.update_signal.connect(self.rubChange.update_value)
        self.usdChange.update_signal.connect(self.usdChange.update_value)

        self.pushButton_1.clicked.connect(self.analysis)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def analysis(self):
        if self.oil == float(self.textEdit_3.toPlainText()):
            return
        elif float(self.textEdit_3.toPlainText()) > self.oil:
            self.usdChange.update_signal.emit(float(str(self.exchange_rate)), float(self.textEdit_1.toPlainText()))
            self.textEdit_2.setText(self.usdChange.value)
            self.textEdit_1.setText(str(float(self.textEdit_1.toPlainText()) + float(self.textEdit_3.toPlainText())))
        else:
            self.rubChange.update_signal.emit(float(str(self.exchange_rate)), float(self.textEdit_2.toPlainText()))
            self.textEdit_1.setText(self.usdChange.value)
            self.textEdit_2.setText(str(float(self.textEdit_2.toPlainText()) + float(self.textEdit_3.toPlainText())))
        self.oil = float(self.textEdit_3.toPlainText())



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Laboratory Work №2"))
        self.pushButton_1.setText(_translate("MainWindow", "Analysis"))
        self.label_1.setText(_translate("MainWindow", "RUB"))
        self.label_2.setText(_translate("MainWindow", "USD"))
        self.label_3.setText(_translate("MainWindow", "BR (Count)"))



class ChangeRub(QObject):
    update_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.value = ''

    def update_value(self, new_value: float, price: float):
        self.value = str(price * new_value)


class ChangeUsd(QObject):
    update_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.value = ''

    def update_value(self, new_value: float, price: float):
        self.value = str(price / new_value)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
