# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SouthWest_Checkin.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(445, 286)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_confirmation = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_confirmation.setGeometry(QtCore.QRect(170, 141, 151, 31))
        self.lineEdit_confirmation.setText("")
        self.lineEdit_confirmation.setObjectName("lineEdit_confirmation")
        self.label_confirmation = QtWidgets.QLabel(self.centralwidget)
        self.label_confirmation.setGeometry(QtCore.QRect(40, 140, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_confirmation.setFont(font)
        self.label_confirmation.setObjectName("label_confirmation")
        self.lineEdit_last_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_last_name.setGeometry(QtCore.QRect(170, 91, 151, 31))
        self.lineEdit_last_name.setObjectName("lineEdit_last_name")
        self.lineEdit_first_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_first_name.setGeometry(QtCore.QRect(170, 50, 151, 31))
        self.lineEdit_first_name.setObjectName("lineEdit_first_name")
        self.label_first_name = QtWidgets.QLabel(self.centralwidget)
        self.label_first_name.setGeometry(QtCore.QRect(40, 60, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_first_name.setFont(font)
        self.label_first_name.setObjectName("label_first_name")
        self.label_last_name = QtWidgets.QLabel(self.centralwidget)
        self.label_last_name.setGeometry(QtCore.QRect(40, 100, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_last_name.setFont(font)
        self.label_last_name.setObjectName("label_last_name")
        self.pushButton_start_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_stop.setGeometry(QtCore.QRect(40, 210, 91, 31))
        self.pushButton_start_stop.setObjectName("pushButton_start_stop")
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(150, 210, 91, 31))
        self.pushButton_exit.setObjectName("pushButton_exit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SouthWest Auto Checkin"))
        self.label_confirmation.setText(_translate("MainWindow", "Confirmation #:"))
        self.label_first_name.setText(_translate("MainWindow", "First Name:"))
        self.label_last_name.setText(_translate("MainWindow", "Last Name:"))
        self.pushButton_start_stop.setText(_translate("MainWindow", "Start"))
        self.pushButton_exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
