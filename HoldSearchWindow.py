# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldSearchWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector




class Ui_Dialog(object):
    def populateTable(self):
        self.c.execute("SELECT id, customer, timestamp FROM hold ORDER BY timestamp DESC")
        self.all_hold = self.c.fetchall()
        self.holdTable.setRowCount(0)
        self.holdTable.setRowCount(len(self.all_hold))
        for i, hold in enumerate(self.all_hold):
            _id, customer, timestamp = hold
            date = timestamp.strftime("%b %d, %Y")
            time = timestamp.strftime("%I:%M:%S %p")
            
            hold_item = QtWidgets.QTableWidgetItem(str(_id))
            self.holdTable.setItem(i, 0, hold_item)
            customer_item = QtWidgets.QTableWidgetItem(str(customer))
            self.holdTable.setItem(i, 1, customer_item)
            date_item = QtWidgets.QTableWidgetItem(str(date))
            self.holdTable.setItem(i, 2, date_item)
            time_item = QtWidgets.QTableWidgetItem(str(time))
            self.holdTable.setItem(i, 3, time_item)
    def setTable(self):
        query = self.customerName.text()
        self.c.execute("SELECT id, customer, timestamp FROM hold ORDER BY timestamp DESC")
        self.all_hold = self.c.fetchall()
        query_result = self.all_hold
        query_result = [x for x in query_result if query.lower() in x[1].lower()]
        self.holdTable.setRowCount(len(query_result))
        for i, hold in enumerate(query_result):
            _id, customer, timestamp = hold
            date = timestamp.strftime("%b %d, %Y")
            time = timestamp.strftime("%I:%M:%S %p")
            
            hold_item = QtWidgets.QTableWidgetItem(str(_id))
            self.holdTable.setItem(i, 0, hold_item)
            customer_item = QtWidgets.QTableWidgetItem(str(customer))
            self.holdTable.setItem(i, 1, customer_item)
            date_item = QtWidgets.QTableWidgetItem(str(date))
            self.holdTable.setItem(i, 2, date_item)
            time_item = QtWidgets.QTableWidgetItem(str(time))
            self.holdTable.setItem(i, 3, time_item)

    def recallItems(self):
        row = self.holdTable.currentRow()
        item = self.holdTable.item(row, 0).text()
        self.c.execute("SELECT product_id, price, quantity FROM hold_product WHERE hold_id = %s", (item, ))
        held_items = self.c.fetchall()
        for i, held_item in enumerate(held_items):
            product_id, price, quantity = held_item
            self.c.execute("SELECT barcode from product where id = %s", (product_id, ))
            barcode = self.c.fetchone()[0]
            self.parent.productTable.addItem(barcode, quantity, self.parent)
            self.Dialog.hide()
            

    def setupUi(self, Dialog, c, parent):
        self.parent = parent
        self.c = c
        self.all_hold = []
        self.Dialog = Dialog
        self.Dialog.setObjectName("Search Hold Sale")
        self.Dialog.setFixedSize(475, 310)
        self.holdTable = QtWidgets.QTableWidget(self.Dialog)
        self.holdTable.setGeometry(QtCore.QRect(8, 50, 451, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.holdTable.setFont(font)
        self.holdTable.setObjectName("holdTable")
        self.holdTable.setColumnCount(4)
        self.holdTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.holdTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.holdTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.holdTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.holdTable.setHorizontalHeaderItem(3, item)
        self.holdTable.verticalHeader().hide()
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.holdTable.sizePolicy().hasHeightForWidth())
        font = QtGui.QFont()
        font.setPointSize(10)
        self.holdTable.setFont(font)
        self.holdTable.setSizePolicy(sizePolicy)
        self.holdTable.setColumnWidth(0, 100)
        self.holdTable.setColumnWidth(1, 140)
        self.holdTable.setColumnWidth(2, 100)
        self.holdTable.setColumnWidth(3, 100)
        header = self.holdTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        
        self.holdTable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.holdTable.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.holdTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.holdTable.setCurrentCell(-1, 0)
        self.holdTable.doubleClicked.connect(self.recallItems)

        self.customerName = QtWidgets.QLineEdit(self.Dialog)
        self.customerName.setGeometry(QtCore.QRect(10, 10, 451, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.customerName.setFont(font)
        self.customerName.setStyleSheet("padding-left: 5px;")
        self.customerName.setObjectName("customerName")
        self.setTable()
        self.customerName.textChanged.connect(self.setTable)
        self.layoutWidget = QtWidgets.QWidget(self.Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(250, 270, 201, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recall = QtWidgets.QLabel(self.layoutWidget)
        self.recall.setStyleSheet("background-color: rgba(0,123,255, 0.9); color: white; border-radius: 5px; border: 1px solid gray;")
        self.recall.setAlignment(QtCore.Qt.AlignCenter)
        self.recall.enterEvent = lambda x: self.recall.setStyleSheet("background-color: rgba(0,123,255, 1); color: white; border-radius: 5px; border: 1px solid gray;")
        self.recall.leaveEvent = lambda x: self.recall.setStyleSheet("background-color: rgba(0,123,255, 0.9); color: white; border-radius: 5px; border: 1px solid gray;")
        
        self.recall.setObjectName("recall")
        self.recall.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.recall.mousePressEvent = lambda x: self.recallItems()
        self.horizontalLayout.addWidget(self.recall)
        self.cancel = QtWidgets.QLabel(self.layoutWidget)

        self.cancel.setStyleSheet("background-color: rgba(220,53,69, 0.9); color: white; border-radius: 5px; border: 1px solid gray;")
        self.cancel.enterEvent = lambda x: self.cancel.setStyleSheet("background-color: rgba(220,53,69, 1); color: white; border-radius: 5px; border: 1px solid gray;")
        self.cancel.leaveEvent = lambda x: self.cancel.setStyleSheet("background-color: rgba(220,53,69, 0.9); color: white; border-radius: 5px; border: 1px solid gray;")
        self.cancel.setAlignment(QtCore.Qt.AlignCenter)
        self.cancel.setObjectName("cancel")
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.cancel)
        self.cancel.mousePressEvent = lambda x: self.Dialog.hide()
        self.setTable()

        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.holdTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Hold ID"))
        item = self.holdTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Customer Name"))
        item = self.holdTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Date"))
        item = self.holdTable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Time"))
        self.customerName.setPlaceholderText(_translate("Dialog", "Customer Name"))
        self.recall.setText(_translate("Dialog", "Recall"))
        self.cancel.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
