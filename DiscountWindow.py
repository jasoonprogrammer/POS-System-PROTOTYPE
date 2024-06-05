# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DiscountWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def valueTester(self):
        value = self.lineEdit.text()
        try:
            float(value)
        except ValueError:
            self.lineEdit.setText(value[:-1])

    def setDiscount(self):
        currRow = self.parent.productTable.currentRow()
        value = self.lineEdit.text()
        value = "{:,.2f}".format(float(value))
        curr_val = self.parent.productTable.item(currRow, 2).text()
        curr_val = float(curr_val)
        if float(self.lineEdit.text()) > curr_val:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Discount Error")
            msg.setText("Discount can't exceed the price")
            msg.exec_()
            del msg
        else:
            self.parent.productTable.modifyCell(currRow, 4, value, alignment = "right")
            self.parent.setOutput()
            self.Dialog.hide()
            self.lineEdit.setText("")
            self.parent.productTable.setSubtotal()
            self.parent.setOutput()

    
    def hideDialog(self):
        self.Dialog.hide()
        self.lineEdit.setText("")

    def setupUi(self, Dialog, **kwargs):
        self.parent = kwargs['parent']
        self.c = kwargs['c']
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Dialog.setFixedSize(316, 154)
        self.Dialog.keyPressEvent = lambda x: self.hideDialog()
        self.widget = QtWidgets.QWidget(self.Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 271, 111))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.textChanged.connect(self.valueTester)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("padding-left: 5px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.setDiscount)
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.ok.setFont(font)
        self.ok.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px;")
        self.ok.setAlignment(QtCore.Qt.AlignCenter)
        self.ok.setObjectName("ok")
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtWidgets.QLabel(self.widget)
        self.cancel.setStyleSheet("background-color: #DC3545; color: white; border-radius: 5px;")
        self.cancel.setAlignment(QtCore.Qt.AlignCenter)
        self.cancel.setObjectName("cancel")
        self.cancel.mousePressEvent = lambda x: self.hideDialog()
        self.ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ok.mousePressEvent = lambda x: self.setDiscount()
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Discount Price"))
        self.label.setText(_translate("Dialog", "Discount for Product "))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "0.00"))
        self.ok.setText(_translate("Dialog", "Ok"))
        self.cancel.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
