from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import subprocess


class Ui_MainWindow(object):
    auth_attempts = 3

    def valuer_call(self):
        MainWindow.hide()
        subprocess.run(['python', 'valuer.py'])

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(286, 217)
        MainWindow.setFixedSize(286, 217)
        MainWindow.setWindowIcon(QtGui.QIcon('student.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(40, 140, 0, 0))
        self.register_button.setObjectName("register_button")
        self.register_button.clicked.connect(self.register)
        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setGeometry(QtCore.QRect(40, 140, 201, 41))
        self.auth_button.setObjectName("auth_button")
        self.auth_button.clicked.connect(self.auth)
        self.login_line = QtWidgets.QLineEdit(self.centralwidget)
        self.login_line.setGeometry(QtCore.QRect(40, 70, 201, 21))
        self.login_line.setObjectName("login_line")
        self.password_line = QtWidgets.QLineEdit(self.centralwidget)
        self.password_line.setGeometry(QtCore.QRect(40, 100, 201, 21))
        self.password_line.setObjectName("password_line")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(120, 20, 41, 41))
        self.logo.setText("")
        self.logo.setTextFormat(QtCore.Qt.AutoText)
        self.logo.setPixmap(QtGui.QPixmap("student.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(95, 120, 121, 21))
        self.label.setStyleSheet("color: rgb(255, 0, 4);")
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация"))
        self.register_button.setText(_translate("MainWindow", "Регистрация"))
        self.auth_button.setText(_translate("MainWindow", "Авторизация"))
        self.login_line.setPlaceholderText(_translate("MainWindow", "Логин"))
        self.password_line.setPlaceholderText(_translate("MainWindow", "Пароль"))

    def action(self):
        self.valuer_call()

    def register(self):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS 
                       users (
                            id INTEGER PRIMARY KEY,
                            login TEXT,
                            pass TEXT
                       )
                       """)
        cursor.execute(f"INSERT INTO users VALUES(NULL,'{self.login_line.text()}','{self.password_line.text()}' )")
        self.label.setStyleSheet("color: rgb(3, 255, 4);")
        self.label.setText("Зарегистрирован.")
        db.commit()
        db.close()

    def auth(self):
        db = sqlite3.connect('database.db')

        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM users WHERE login = '{self.login_line.text()}' AND pass = '{self.password_line.text()}'")
        if cursor.fetchone() != None:
            print('Вы вошли в аккаунт')
            self.action()
        else:
            self.attempts()
    
        db.commit()
        db.close()

    def attempts(self):
        if self.auth_attempts <= 0:
            self.auth_button.setEnabled(False)
        else: 
            self.label.setStyleSheet("color: rgb(255, 0, 4);")
            self.label.setText(f'Осталось попыток: {self.auth_attempts}')
            self.auth_attempts -=1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())