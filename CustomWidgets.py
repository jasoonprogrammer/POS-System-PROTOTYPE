from PyQt5 import QtCore, QtGui, QtWidgets


def isFloat(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def isInt(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


ARROW_UP = 16777235
ARROW_DOWN = 16777237
NUMPAD_PLUS = 43
NUMPAD_MINUS = 45

class HoverLabel(QtWidgets.QLabel):
    
    def setHover(self, eve):
        self.setPixmap(QtGui.QPixmap(self.hover_image))
    
    def setDefault(self, eve):
        self.setPixmap(QtGui.QPixmap(self.initial_image))

        
    def __init__(self, parent, initial_image, size, objectName, mount = None):
        super().__init__(parent)
        self.size = size
        self.initial_image = initial_image
        self.setScaledContents(True)
        self.hover_image = self.initial_image.replace(".png", "_Hovered.png")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.enterEvent = self.setHover
        self.leaveEvent = self.setDefault
        self.setPixmap(QtGui.QPixmap(self.initial_image))
        self.setMinimumSize(QtCore.QSize(self.size[0], self.size[1]))
        self.setMaximumSize(QtCore.QSize(self.size[0], self.size[1]))
        self.setBaseSize(QtCore.QSize(self.size[0], self.size[1]))
        self.setObjectName(objectName)
        if mount != None:
            self.mount = mount
            self.mount.addWidget(self)

class CustomTableWidget(QtWidgets.QTableWidget):
    def setSubtotal(self):
        row, _, price = self.grabCurrent(column = 2)
        _, _, qty = self.grabCurrent(column = 3)
        _, _, discount = self.grabCurrent(column = 4)
        total = float(price) * int(qty) - float(discount)
        self.modifyCell(row, 5, "{:,.2f}".format(total), alignment = "right")

    def priceChange(self, newPrice, **kwargs):
        parent = kwargs['parent']
        row, col, val = self.grabCurrent(column = 2)
        self.modifyCell(row, 4, col, newPrice, alignment = "right")
    
    def grabCurrent(self, column = 0):
        row = self.currentRow()
        col = column
        value = self.item(row, col).text()
        return (row, col, value)
        

    def modifyCell(self, row, index, value, alignment = "left"):
        item = QtWidgets.QTableWidgetItem(str(value))
        if alignment.lower() == "right":
            align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        elif alignment.lower() == "left":
            align = QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
        elif alignment.lower() == "center":
            align = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        else:
            raise ValueError(f"{alignment} is not a valid alignment")
        item.setTextAlignment(align)
        self.setItem(row, index, item)
        

    def bindKeys(self, eve, **kwargs):
        parent = kwargs['parent']
        print(eve.key())
        if eve.key() == QtCore.Qt.Key_F2:
            parent.setDiscount()
        if eve.key() == 43:
            self.addQty(parent = parent)
        if eve.key() == 45:
            self.subQty(parent = parent)
        if eve.key() == 16777264:
            parent.paymentArea.setFocus()

    def holdSale(self, **kwargs):
        MainWindow = kwargs['MainWindow']
        parent = kwargs['parent']
        cashier_id = kwargs['cashier_id']
        rows = self.rowCount()
        if rows > 0:
            buttonReply = QtWidgets.QMessageBox.question(MainWindow, 'Confirm Void', "Void this product from list?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                parent.c.execute("INSERT INTO hold (cashier_id) VALUES (%s)", (cashier_id, ))
                parent.conn.commit()
                hold_id = parent.c.lastrowid
                for row in range(rows):
                    anon = lambda x: self.item(row, x).text()
                    arr = {"barcode": anon(0), "price": anon(2), "qty": anon(3), "discount": anon(4)}
                    parent.c.execute("SELECT id FROM product WHERE barcode = %s", (anon(0),))
                    product_id = parent.c.fetchone()[0]
                    parent.c.execute("INSERT INTO hold_product (hold_id, product_id, price, quantity) VALUES (%s, %s, %s, %s)",
                            (hold_id, product_id, anon(2), anon(3),))
                    parent.conn.commit()
                self.setRowCount(0)
                parent.paymentArea.setText("")
                parent.setOutput()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("No items in the table")
            msg.setText("Can't hold a table if it's empty.")
            msg.exec_()
            del msg

    def addQty(self, **kwargs):
        try:
            parent = kwargs['parent']
        except KeyError:
            parent = None
        row = self.currentRow()
        if row >= 0:
            qty = self.item(row, 3).text()
            qty = int(qty)
            qty += 1
            price = self.item(row, 2).text()
            total = float(price) * qty
            total = "{:,.2f}".format(total)
            align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
            qty_item = QtWidgets.QTableWidgetItem(str(qty))
            qty_item.setTextAlignment(align)
            total_item = QtWidgets.QTableWidgetItem(str(total))
            total_item.setTextAlignment(align)
            self.setItem(row, 3, qty_item)
            self.setItem(row, 5, total_item)
        
        if kwargs['parent']:
            parent.setOutput()

    def subQty(self, **kwargs):
        try:
            parent = kwargs['parent']
        except KeyError:
            parent = None
        row = self.currentRow()
        if row >= 0:
            qty = self.item(row, 3).text()
            qty = int(qty)
            if qty > 1:
                qty -= 1
                price = self.item(row, 2).text()
                total = float(price) * qty
                total = "{:,.2f}".format(total)
                align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                qty_item = QtWidgets.QTableWidgetItem(str(qty))
                qty_item.setTextAlignment(align)
                total_item = QtWidgets.QTableWidgetItem(str(total))
                total_item.setTextAlignment(align)
                self.setItem(row, 3, qty_item)
                self.setItem(row, 5, total_item)
        if parent:
            parent.setOutput()


    def keyCapture(self, eve, parent):
        if eve.key() == NUMPAD_PLUS:
            self.addQty()
        elif eve.key() == NUMPAD_MINUS:
            self.subQty()
        if eve.key() == ARROW_UP:
            currentRow = self.currentRow()
            if self.currentRow() < 0:
                self.setCurrentCell(self.rowCount() - 1, 1)
            else:
                self.setCurrentCell(self.currentRow() - 1, 1)
            parent.capturedKeys.clear()
        if eve.key() == ARROW_DOWN:
            row = self.currentRow()
            self.setCurrentCell(row + 1, 1)
            parent.capturedKeys.clear()
        parent.setOutput()
        if eve.key() == QtCore.Qt.Key_Escape:
            parent.barcodeArea.setFocus()
    def addItem(self, barcode, qty, parent):
        if parent.paymentArea.isEnabled() == False:
            parent.paymentArea.setEnabled(True)
            parent.paymentArea.setText("")
        parent.c.execute("SELECT name, price FROM product WHERE barcode = %s", (barcode,))
        result = parent.c.fetchone()
        if result:
            row = self.rowCount()
            self.setRowCount(row + 1)
            total = qty * result[1]
            arr = [barcode, result[0], "{:,.2f}".format(result[1]), qty, 0, "{:,.2f}".format(total)]
            row_range = list(range(row))
            row_range.reverse()
            for r in row_range:
                for col in range(6):
                    if col == 1:
                        align = QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
                    else:
                        align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                    text = self.item(r, col).text()
                    item = QtWidgets.QTableWidgetItem(str(text))
                    item.setTextAlignment(align)
                    self.setItem(r + 1, col, item)
            for i, col in enumerate(arr):
                if i == 1:
                    align = QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
                else:
                    align = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                item = QtWidgets.QTableWidgetItem(str(col))
                item.setTextAlignment(align)
                self.setItem(0, i, item)
            parent.setOutput()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Barcode not found")
            msg.setText("No product is registered with this barcode")
            msg.exec_()
            del msg

    def removeItem(self, **kwargs):
        MainWindow = kwargs['MainWindow']
        if self.rowCount() > 0:
            if self.currentRow() < 0:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("No item selected")
                msg.setText("Please select an item.")
                msg.exec_()
                del msg
            else:
                buttonReply = QtWidgets.QMessageBox.question(MainWindow, 'Confirm Void', "Void this product from list?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if buttonReply == QtWidgets.QMessageBox.Yes:
                    row = self.currentRow()
                    self.removeRow(row)
                    self.clearFocus()
                    kwargs['parent'].barcodeArea.setFocus()
                del buttonReply
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("No more items")
            msg.setText("Can't remove from an empty table.")
            msg.exec_()
            del msg