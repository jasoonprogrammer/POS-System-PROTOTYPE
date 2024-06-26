# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AccountManagement.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from cryptography.fernet import Fernet
class Ui_Form(object):
    def resetPassword(self):
        index = self.usernameCbo.currentIndex()
        username = self.actives[index]
        password1 = self.resetPasswordEntry.text()
        password2 = self.resetConfirmPasswordEntry.text()
        if password1 == password2:
            if len(password1) < 5:
                self.showError("Length error!", "Passwords needs to be atleast 5 characters")
            else:
                hash_key = Fernet.generate_key()
                f = Fernet(hash_key)
                token = f.encrypt(password1.encode())
                self.parent.c.execute("UPDATE user SET password = %s, hash_key = %s WHERE username = %s", (token, hash_key, username, ))
                self.parent.conn.commit()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Password updated!")
                msg.setText("Password updated successfully")
                msg.exec_()




        else:
            self.showError("Passwords don't match!", "Your passwords don't match.")

    def setUpdate(self, index):
        username = self.actives[index]
        self.parent.c.execute("SELECT username, first_name, last_name FROM user WHERE username = %s", (username, ))
        username, first_name, last_name = self.parent.c.fetchone()
        self.resetFirstNameEntry.setText(first_name)
        self.resetLastNameEntry.setText(last_name)

        
    def activateAccount(self):
        index = self.activateUsernameCbo.currentIndex()
        username = self.usernames[index]
        self.parent.c.execute("UPDATE user SET is_active = 1 WHERE username = %s", (username, ))
        self.parent.conn.commit()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Activated!")
        msg.setText("Account activated successfully")
        msg.exec_()
        del msg
        self.setActivateDeactivate(self.activateUsernameCbo.currentIndex())
        self.refreshUsernames()

    def deactivateAccount(self):
        index = self.activateUsernameCbo.currentIndex()
        username = self.usernames[index]
        self.parent.c.execute("UPDATE user SET is_active = 0 WHERE username = %s", (username, ))
        self.parent.conn.commit()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Deactivated!")
        msg.setText("Account deactivated successfully")
        msg.exec_()
        del msg
        self.setActivateDeactivate(self.activateUsernameCbo.currentIndex())
        self.refreshUsernames()
        
    def setActivateDeactivate(self, index):
        username = self.usernames[index]
        self.parent.c.execute("SELECT is_active FROM user WHERE username = %s", (username, ))
        is_active = self.parent.c.fetchone()[0]
        if is_active:
            self.activateDeactivateButton.hide()
            self.activateDeactivateButton_2.show()
        else:
            self.activateDeactivateButton.show()
            self.activateDeactivateButton_2.hide()


    
    def refreshUsernames(self):
        self.parent.c.execute("SELECT username, is_active from user")
        users = self.parent.c.fetchall()
        self.usernames = [x[0] for x in users]
        self.usernameCbo.clear()
        self.actives = [x[0] for x in users if x[1] == 1]
        self.usernameCbo.addItems(self.actives)
        self.activateUsernameCbo.clear()
        self.activateUsernameCbo.addItems([x[0] for x in users])
    def showError(self, title, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.exec_()
        del msg
    def createAccount(self):
        username = self.usernameEntry.text()
        password = self.passwordEntry.text()
        confirmPassword = self.confirmPasswordEntry.text()
        firstName = self.firstNameEntry.text()
        lastName = self.lastNameEntry.text()
        self.parent.c.execute("select id from user where username = %s", (username, ))
        exist = self.parent.c.fetchone()
        if exist:
            self.showError("Already registered", "Account with the username {} is already registered".format(username))
        elif len(username) < 5:
            self.showError("Length Error", "Username should be atleast 5 characters")
        elif len(password) < 5:
            self.showError("Length Error", "Password should be atleast 5 characters")
        elif len(firstName) < 3:
            self.showError("Length Error", "First Name must be atleast 3 characters")
        elif len(lastName) < 3:
            self.showError("Length Error", "Last Name must be atleast 3 characters")
        elif password != confirmPassword:
            self.showError("Password don't match", "Your passwords don't match")
        else:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encMessage = fernet.encrypt(password.encode())
            self.parent.c.execute("INSERT INTO user (username, password, hash_key, first_name, last_name) VALUES (%s, %s, %s, %s, %s)", (username, encMessage, key, firstName.title(), lastName.title()))
            self.parent.conn.commit()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Account Created Successfully")
            msg.setText("You can now use the account to login.")
            msg.exec_()
            del msg
            self.usernameEntry.setText("")
            self.passwordEntry.setText("")
            self.confirmPasswordEntry.setText("")
            self.firstNameEntry.setText("")
            self.lastNameEntry.setText("")
        
            
    def setupUi(self, Form, parent):
        self.parent = parent
        Form.setObjectName("Form")
        Form.setFixedSize(380, 500)
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.closeEvent = lambda x: parent.Form.show()
        self.usernames = []
        self.actives = []
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget_3 = QtWidgets.QWidget(self.tab)
        self.layoutWidget_3.setGeometry(QtCore.QRect(50, 320, 271, 71))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lastNameLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.lastNameLabel.setFont(font)
        self.lastNameLabel.setObjectName("lastNameLabel")
        self.verticalLayout_4.addWidget(self.lastNameLabel)
        self.lastNameEntry = QtWidgets.QLineEdit(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastNameEntry.sizePolicy().hasHeightForWidth())
        self.lastNameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.lastNameEntry.setFont(font)
        self.lastNameEntry.setStyleSheet("padding-left: 5px;")
        self.lastNameEntry.setObjectName("lastNameEntry")
        self.verticalLayout_4.addWidget(self.lastNameEntry)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setGeometry(QtCore.QRect(50, 400, 271, 41))
        self.pushButton.clicked.connect(self.createAccount)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {background-color: #198754; color: white; border-radius: 8px;} QPushButton:hover {background-color: #146C43, color: white; border-radius: 8px;}")
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(50, 250, 271, 71))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.firstNameLabel = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.firstNameLabel.setFont(font)
        self.firstNameLabel.setObjectName("firstNameLabel")
        self.verticalLayout_3.addWidget(self.firstNameLabel)
        self.firstNameEntry = QtWidgets.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firstNameEntry.sizePolicy().hasHeightForWidth())
        self.firstNameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.firstNameEntry.setFont(font)
        self.firstNameEntry.setStyleSheet("padding-left: 5px;")
        self.firstNameEntry.setObjectName("firstNameEntry")
        self.verticalLayout_3.addWidget(self.firstNameEntry)
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 20, 271, 89))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.usernameLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.verticalLayout.addWidget(self.usernameLabel)
        self.usernameEntry = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameEntry.sizePolicy().hasHeightForWidth())
        self.usernameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.usernameEntry.setFont(font)
        self.usernameEntry.setStyleSheet("padding-left: 5px;")
        self.usernameEntry.setObjectName("usernameEntry")
        self.verticalLayout.addWidget(self.usernameEntry)
        self.layoutWidget1 = QtWidgets.QWidget(self.tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 110, 271, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.passwordLabel = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.verticalLayout_2.addWidget(self.passwordLabel)
        self.passwordEntry = QtWidgets.QLineEdit(self.layoutWidget1)
        self.passwordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordEntry.sizePolicy().hasHeightForWidth())
        self.passwordEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.passwordEntry.setFont(font)
        self.passwordEntry.setStyleSheet("padding-left: 5px;")
        self.passwordEntry.setObjectName("passwordEntry")
        self.verticalLayout_2.addWidget(self.passwordEntry)
        self.layoutWidget_4 = QtWidgets.QWidget(self.tab)
        self.layoutWidget_4.setGeometry(QtCore.QRect(50, 180, 271, 71))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.confirmPasswordLabel = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.confirmPasswordLabel.setFont(font)
        self.confirmPasswordLabel.setObjectName("confirmPasswordLabel")
        self.verticalLayout_5.addWidget(self.confirmPasswordLabel)
        self.confirmPasswordEntry = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.confirmPasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirmPasswordEntry.sizePolicy().hasHeightForWidth())
        self.confirmPasswordEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.confirmPasswordEntry.setFont(font)
        self.confirmPasswordEntry.setStyleSheet("padding-left: 5px;")
        self.confirmPasswordEntry.setObjectName("confirmPasswordEntry")
        self.verticalLayout_5.addWidget(self.confirmPasswordEntry)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget_5 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_5.setGeometry(QtCore.QRect(50, 320, 271, 71))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.resetLastNameLabel = QtWidgets.QLabel(self.layoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        
        self.tab.setTabOrder(self.usernameEntry, self.passwordEntry)
        self.tab.setTabOrder(self.passwordEntry, self.confirmPasswordEntry)
        self.tab.setTabOrder(self.confirmPasswordEntry, self.firstNameEntry)
        self.tab.setTabOrder(self.firstNameEntry, self.lastNameEntry)
        self.tab.setTabOrder(self.lastNameEntry, self.pushButton)
        self.resetLastNameLabel.setFont(font)
        self.resetLastNameLabel.setObjectName("resetLastNameLabel")
        self.verticalLayout_6.addWidget(self.resetLastNameLabel)
        self.resetLastNameEntry = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.resetLastNameEntry.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetLastNameEntry.sizePolicy().hasHeightForWidth())
        self.resetLastNameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetLastNameEntry.setFont(font)
        self.resetLastNameEntry.setStyleSheet("padding-left: 5px;")
        self.resetLastNameEntry.setObjectName("resetLastNameEntry")
        self.verticalLayout_6.addWidget(self.resetLastNameEntry)
        self.layoutWidget_6 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_6.setGeometry(QtCore.QRect(50, 20, 271, 89))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.resetUsernameLabel = QtWidgets.QLabel(self.layoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetUsernameLabel.setFont(font)
        self.resetUsernameLabel.setObjectName("resetUsernameLabel")
        self.verticalLayout_7.addWidget(self.resetUsernameLabel)
        self.usernameCbo = QtWidgets.QComboBox(self.layoutWidget_6)
        self.usernameCbo.setFont(font)
        self.usernameCbo.setStyleSheet("padding-left: 5px;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameCbo.sizePolicy().hasHeightForWidth())
        self.usernameCbo.setSizePolicy(sizePolicy)
        self.usernameCbo.setObjectName("usernameCbo")
        self.usernameCbo.currentIndexChanged.connect(self.setUpdate)
        self.verticalLayout_7.addWidget(self.usernameCbo)
        self.layoutWidget_7 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_7.setGeometry(QtCore.QRect(50, 180, 271, 71))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget_7)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.resetConfirmPasswordLabel = QtWidgets.QLabel(self.layoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetConfirmPasswordLabel.setFont(font)
        self.resetConfirmPasswordLabel.setObjectName("resetConfirmPasswordLabel")
        self.verticalLayout_8.addWidget(self.resetConfirmPasswordLabel)
        self.resetConfirmPasswordEntry = QtWidgets.QLineEdit(self.layoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetConfirmPasswordEntry.sizePolicy().hasHeightForWidth())
        self.resetConfirmPasswordEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetConfirmPasswordEntry.setFont(font)
        self.resetConfirmPasswordEntry.setStyleSheet("padding-left: 5px;")
        self.resetConfirmPasswordEntry.setObjectName("resetConfirmPasswordEntry")
        self.resetConfirmPasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout_8.addWidget(self.resetConfirmPasswordEntry)
        self.layoutWidget_8 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_8.setGeometry(QtCore.QRect(50, 250, 271, 71))
        self.layoutWidget_8.setObjectName("layoutWidget_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.layoutWidget_8)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.resetFirstNameLabel = QtWidgets.QLabel(self.layoutWidget_8)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetFirstNameLabel.setFont(font)
        self.resetFirstNameLabel.setObjectName("resetFirstNameLabel")
        self.verticalLayout_9.addWidget(self.resetFirstNameLabel)
        self.resetFirstNameEntry = QtWidgets.QLineEdit(self.layoutWidget_8)
        self.resetFirstNameEntry.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetFirstNameEntry.sizePolicy().hasHeightForWidth())
        self.resetFirstNameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetFirstNameEntry.setFont(font)
        self.resetFirstNameEntry.setStyleSheet("padding-left: 5px;")
        self.resetFirstNameEntry.setObjectName("resetFirstNameEntry")
        self.verticalLayout_9.addWidget(self.resetFirstNameEntry)
        self.layoutWidget_9 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_9.setGeometry(QtCore.QRect(50, 110, 271, 71))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.layoutWidget_9)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.resetPasswordLabel = QtWidgets.QLabel(self.layoutWidget_9)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetPasswordLabel.setFont(font)
        self.resetPasswordLabel.setObjectName("resetPasswordLabel")
        self.verticalLayout_10.addWidget(self.resetPasswordLabel)
        self.resetPasswordEntry = QtWidgets.QLineEdit(self.layoutWidget_9)
        self.resetPasswordEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetPasswordEntry.sizePolicy().hasHeightForWidth())
        self.resetPasswordEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.resetPasswordEntry.setFont(font)
        self.resetPasswordEntry.setStyleSheet("padding-left: 5px;")
        self.resetPasswordEntry.setObjectName("resetPasswordEntry")
        self.verticalLayout_10.addWidget(self.resetPasswordEntry)
        self.resetPasswordButton = QtWidgets.QPushButton(self.tab_2)
        self.resetPasswordButton.setGeometry(QtCore.QRect(50, 400, 271, 41))
        self.resetPasswordButton.clicked.connect(self.resetPassword)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.resetPasswordButton.setFont(font)
        self.resetPasswordButton.setStyleSheet("QPushButton {background-color: #198754; color: white; border-radius: 8px;} QPushButton:hover {background-color: #146C43, color: white; border-radius: 8px;}")
        self.resetPasswordButton.setObjectName("resetPasswordButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.layoutWidget_10 = QtWidgets.QWidget(self.tab_3)
        self.layoutWidget_10.setGeometry(QtCore.QRect(50, 110, 271, 89))
        self.layoutWidget_10.setObjectName("layoutWidget_10")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.layoutWidget_10)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.activateUsernameLabel = QtWidgets.QLabel(self.layoutWidget_10)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.activateUsernameLabel.setFont(font)
        self.activateUsernameLabel.setObjectName("activateUsernameLabel")
        self.verticalLayout_11.addWidget(self.activateUsernameLabel)
        self.activateUsernameCbo = QtWidgets.QComboBox(self.layoutWidget_10)
        self.activateUsernameCbo.setFont(font)
        self.activateUsernameCbo.setStyleSheet("padding-left: 5px;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activateUsernameCbo.sizePolicy().hasHeightForWidth())
        self.activateUsernameCbo.setSizePolicy(sizePolicy)
        self.activateUsernameCbo.setObjectName("activateUsernameCbo")
        self.activateUsernameCbo.currentIndexChanged.connect(self.setActivateDeactivate)
        self.verticalLayout_11.addWidget(self.activateUsernameCbo)
        self.activateDeactivateButton = QtWidgets.QPushButton(self.tab_3)
        self.activateDeactivateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.activateDeactivateButton.setGeometry(QtCore.QRect(50, 220, 271, 41))
        self.activateDeactivateButton.setObjectName("activateDeactivateButton")
        self.activateDeactivateButton.setStyleSheet("""
            QPushButton {background-color: #146C43; color: white; border-radius: 8px; }
            QPushButton:active {background-color: #0F5132; color: white; border-radius: 8px; }
            """)
        self.activateDeactivateButton.clicked.connect(self.activateAccount)
        self.activateDeactivateButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.activateDeactivateButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.activateDeactivateButton_2.setGeometry(QtCore.QRect(50, 220, 271, 41))
        self.activateDeactivateButton_2.setObjectName("activateDeactivateButton_2")
        self.activateDeactivateButton_2.setStyleSheet("""
            QPushButton {background-color: #B02A37; color: white; border-radius: 8px; }
            QPushButton:active {background-color: #842029; color: white; border-radius: 8px; }
            """)
        self.activateDeactivateButton_2.clicked.connect(self.deactivateAccount)
        self.activateDeactivateButton_2.hide()
        
        
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.usernameEntry, self.passwordEntry)
        Form.setTabOrder(self.passwordEntry, self.firstNameEntry)
        Form.setTabOrder(self.firstNameEntry, self.lastNameEntry)
        Form.setTabOrder(self.lastNameEntry, self.pushButton)
        self.refreshUsernames()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Account"))
        self.lastNameLabel.setText(_translate("Form", "Last Name"))
        self.pushButton.setText(_translate("Form", "Create Account"))
        self.firstNameLabel.setText(_translate("Form", "First Name"))
        self.usernameLabel.setText(_translate("Form", "Username"))
        self.passwordLabel.setText(_translate("Form", "Password"))
        self.confirmPasswordLabel.setText(_translate("Form", "Confirm Password"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Create Account"))
        self.resetLastNameLabel.setText(_translate("Form", "Last Name"))
        self.resetUsernameLabel.setText(_translate("Form", "Username"))
        self.resetConfirmPasswordLabel.setText(_translate("Form", "Confirm Password"))
        self.resetFirstNameLabel.setText(_translate("Form", "First Name"))
        self.resetPasswordLabel.setText(_translate("Form", "New Password"))
        self.resetPasswordButton.setText(_translate("Form", "Reset Password"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Reset Password"))
        self.activateUsernameLabel.setText(_translate("Form", "Username"))
        self.activateDeactivateButton.setText(_translate("Form", "Activate"))
        self.activateDeactivateButton_2.setText(_translate("Form", "Deactivate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Activate/Deactive Account"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    try:
        conn = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "production")
        self.parent.c = conn.cursor()
    except:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Connection Error")
        msg.setText("Please start your localhost")
        msg.exec_()
        del msg
        exit()
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
