# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testmain.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_MainWindow(object):
    def goBack(self):
        self.parent.Form.show()

    def searchItem(self):
        text = self.lineEdit.text()
        current = -1
        for i, result in enumerate(self.results):
            if result[1] == text or text in result[2].lower():
                current = i
        self.tableWidget.setCurrentCell(current, 0)

    def saveEditTable(self):
        barcode = self.barcodeEntry.text()
        name = self.nameEntry.text()
        category = self.nameEntry_2.text()
        price = self.priceEntry.text()
        stock = self.stockEntry.text()
        if barcode == "" or name == "" or category == "" or price == "" or stock == "":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle("Empty fields found")
            msg.setText("Can't leave a field empty")
            msg.exec_()
            self.barcodeEntry.setFocus()
        else:
            if self.barcodeEntry.isEnabled() == False:
                self.c.execute("UPDATE product SET name = %s, category = %s, price = %s, stock = %s WHERE barcode = %s", (name, category, price, stock, barcode, ))
                self.parent.conn.commit()
                self.cancelEditTable()
                self.setTable()
                self.barcodeEntry.setFocus()
            else:
                buttonReply = QtWidgets.QMessageBox.question(self.MainWindow, 'Confirm Save', "Save this edit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
                if buttonReply == QtWidgets.QMessageBox.Yes:
                    self.c.execute("SELECT barcode from product where barcode = %s", (barcode, ))
                    r = self.c.fetchone()
                    if not r:
                        self.c.execute("INSERT INTO product (barcode, name, category, price, stock) VALUES (%s, %s, %s, %s, %s)", (barcode, name, category, price, stock,))
                        self.parent.conn.commit()
                        self.cancelEditTable()
                        self.setTable()
                        self.barcodeEntry.setFocus()
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setWindowTitle("Already registered")
                        msg.setText("This barcode is already registered")
                        msg.exec_()
                        self.barcodeEntry.setFocus()

    def cancelEditTable(self):
        self.barcodeEntry.setEnabled(True)
        self.barcodeEntry.setText("")
        self.nameEntry.setText("")
        self.nameEntry_2.setText("")
        self.priceEntry.setText("")
        self.stockEntry.setText("")
    def editTable(self):
        row = self.tableWidget.currentRow()
        data = []
        for i in range(5):
            value = self.tableWidget.item(row, i).text()
            data.append(value)
        barcode, name, category, price, stock = data
        self.barcodeEntry.setText(str(barcode))
        self.nameEntry.setText(name)
        self.nameEntry_2.setText(category)
        self.priceEntry.setText("{:,.2f}".format(float(price)))
        self.stockEntry.setText(str(stock))
        self.barcodeEntry.setEnabled(False)
        
    def setTable(self):
        self.c.execute("SELECT id, barcode, name, category, price, stock from product")
        self.results = self.c.fetchall()
        self.completer = QtWidgets.QCompleter(self.categories)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.nameEntry_2.setCompleter(self.completer)
        self.results.sort(key = lambda x: x[2])
        self.results.sort(key = lambda x: x[3])
        self.tableWidget.setRowCount(len(self.results))
        for row, result in enumerate(self.results):
            for col, item in enumerate(result[1:]):
                if col == 3:
                    item = "{:,.2f}".format(float(item))
                if col >= 3:
                    align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                else:
                    align = QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
                item = QtWidgets.QTableWidgetItem(str(item))
                item.setTextAlignment(align)
                self.tableWidget.setItem(row, col, item)
    def floatTester(self, target):
        text = target.text()
        try:
            float(text)
        except ValueError:
            target.setText(text[:-1])

    def intTester(self, target):
        text = target.text()
        try:
            int(text)
        except ValueError:
            target.setText(text[:-1])

    def setupUi(self, MainWindow, parent):
        self.parent = parent
        self.c = self.parent.c
        self.c.execute("SELECT id, barcode, name, category, price, stock from product")
        self.results = self.c.fetchall()
        
        self.categories = set([x[3] for x in self.results])
        self.names = [x[2] for x in self.results]
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setFixedSize(1200, 400)
        self.results = []
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 891, 31))
        self.lineEdit.textChanged.connect(self.searchItem)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("padding-left: 5px;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(910, 160, 261, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nameLabel_2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel_2.sizePolicy().hasHeightForWidth())
        self.nameLabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.nameLabel_2.setFont(font)
        self.nameLabel_2.setObjectName("nameLabel_2")
        self.verticalLayout_3.addWidget(self.nameLabel_2)
        self.nameEntry_2 = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameEntry_2.sizePolicy().hasHeightForWidth())
        self.nameEntry_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.nameEntry_2.setFont(font)
        self.nameEntry_2.setStyleSheet("padding-left: 5px;")
        self.nameEntry_2.setText("")
        self.nameEntry_2.setObjectName("nameEntry_2")
        self.completer = QtWidgets.QCompleter(self.categories)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.nameEntry_2.setCompleter(self.completer)
        self.verticalLayout_3.addWidget(self.nameEntry_2)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(910, 40, 261, 51))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.barcodeLabel = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.barcodeLabel.sizePolicy().hasHeightForWidth())
        self.barcodeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.barcodeLabel.setFont(font)
        self.barcodeLabel.setObjectName("barcodeLabel")
        self.verticalLayout.addWidget(self.barcodeLabel)
        self.barcodeEntry = QtWidgets.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.barcodeEntry.sizePolicy().hasHeightForWidth())
        self.barcodeEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.barcodeEntry.setFont(font)
        self.barcodeEntry.setStyleSheet("padding-left: 5px;")
        self.barcodeEntry.setText("")
        self.barcodeEntry.setObjectName("barcodeEntry")
        self.barcodeEntry.textChanged.connect(lambda: self.intTester(self.barcodeEntry))
        self.verticalLayout.addWidget(self.barcodeEntry)
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(910, 100, 261, 51))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.nameLabel = QtWidgets.QLabel(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.verticalLayout_2.addWidget(self.nameLabel)
        self.nameEntry = QtWidgets.QLineEdit()
        self.nameCompleter = QtWidgets.QCompleter(self.names)
        self.nameCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.nameEntry.setCompleter(self.nameCompleter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameEntry.sizePolicy().hasHeightForWidth())
        self.nameEntry.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.nameEntry.setFont(font)
        self.nameEntry.setStyleSheet("padding-left: 5px;")
        self.nameEntry.setText("")
        self.nameEntry.setObjectName("nameEntry")
        self.verticalLayout_2.addWidget(self.nameEntry)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.doubleClicked.connect(self.editTable)
        
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 891, 291))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 395)
        self.tableWidget.setColumnWidth(2, 175)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(910, 290, 261, 31))
        self.saveButton.clicked.connect(self.saveEditTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.setStyleSheet("background-color:green; color: white; border-radius: 5px; border: 1px solid black;")
        self.saveButton.setObjectName("saveButton")
        self.stockEntry = QtWidgets.QLineEdit(self.centralwidget)
        self.stockEntry.setGeometry(QtCore.QRect(1050, 240, 121, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.stockEntry.setFont(font)
        self.stockEntry.setStyleSheet("padding-left: 5px;")
        self.stockEntry.setText("")
        self.stockEntry.setObjectName("stockEntry")
        self.stockEntry.textChanged.connect(lambda: self.intTester(self.stockEntry))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.priceLabel = QtWidgets.QLabel(self.centralwidget)
        self.priceLabel.setGeometry(QtCore.QRect(910, 220, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.priceLabel.setFont(font)
        self.priceLabel.setObjectName("priceLabel")
        self.priceEntry = QtWidgets.QLineEdit(self.centralwidget)
        self.priceEntry.setGeometry(QtCore.QRect(910, 240, 121, 35))
        self.priceEntry.textChanged.connect(lambda: self.floatTester(self.priceEntry))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.priceEntry.setFont(font)
        self.priceEntry.setStyleSheet("padding-left: 5px;")
        self.priceEntry.setText("")
        self.priceEntry.setObjectName("priceEntry")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(910, 340, 261, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.editButton = QtWidgets.QPushButton(self.splitter)
        self.editButton.clicked.connect(self.editTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy)
        self.editButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.editButton.setStyleSheet("background-color: rgba(0,123,255, 0.9); color: white; border-radius: 5px; border:1px solid black;")
        self.editButton.setObjectName("editButton")
        self.editButton.enterEvent = lambda x: self.editButton.setStyleSheet("background-color: rgba(0,123,255, 1); color: white; border-radius: 5px; border:1px solid black;")
        self.editButton.leaveEvent = lambda x: self.editButton.setStyleSheet("background-color: rgba(0,123,255, 0.9); color: white; border-radius: 5px; border:1px solid black;")        
        self.cancelButton = QtWidgets.QPushButton(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelButton.setStyleSheet("background-color: rgba(220,53,69, 0.9); color: white; border-radius: 5px; border: 1px solid black;")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.cancelEditTable)
        self.stockLabel = QtWidgets.QLabel(self.centralwidget)
        self.stockLabel.setGeometry(QtCore.QRect(1050, 220, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.stockLabel.setFont(font)
        self.stockLabel.setObjectName("stockLabel")
        self.MainWindow.setCentralWidget(self.centralwidget)
        
        self.MainWindow.setTabOrder(self.barcodeEntry, self.nameEntry)
        self.MainWindow.setTabOrder(self.nameEntry, self.nameEntry_2)
        self.MainWindow.setTabOrder(self.nameEntry_2, self.priceEntry)
        self.MainWindow.setTabOrder(self.priceEntry, self.stockEntry)
        self.MainWindow.setTabOrder(self.stockEntry, self.lineEdit)
        self.MainWindow.setTabOrder(self.lineEdit, self.saveButton)
        self.MainWindow.setTabOrder(self.saveButton, self.editButton)
        self.MainWindow.setTabOrder(self.editButton, self.cancelButton)
        self.MainWindow.setTabOrder(self.cancelButton, self.tableWidget)
        self.MainWindow.closeEvent = lambda x: self.goBack()

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Product Management"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Barcode or Product Name"))
        self.nameLabel_2.setText(_translate("MainWindow", "Category"))
        self.barcodeLabel.setText(_translate("MainWindow", "Barcode"))
        self.nameLabel.setText(_translate("MainWindow", "Product Name"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Barcode"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Product Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Category"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Stock"))
        self.saveButton.setText(_translate("MainWindow", "Save Item"))
        self.label.setText(_translate("MainWindow", "Product Search"))
        self.priceLabel.setText(_translate("MainWindow", "Price"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.stockLabel.setText(_translate("MainWindow", "Stock"))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
