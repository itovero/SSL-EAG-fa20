# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'materials_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_materials_table(object):
    def setupUi(self, materials_table):
        materials_table.setObjectName("materials_table")
        materials_table.resize(1024, 343)
        self.pushButton = QtWidgets.QPushButton(materials_table)
        self.pushButton.setGeometry(QtCore.QRect(890, 280, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(materials_table)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 961, 241))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 6, item)

        self.retranslateUi(materials_table)
        QtCore.QMetaObject.connectSlotsByName(materials_table)

    def retranslateUi(self, materials_table):
        _translate = QtCore.QCoreApplication.translate
        materials_table.setWindowTitle(_translate("materials_table", "materials_table"))
        self.pushButton.setText(_translate("materials_table", "Done"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("materials_table", "Material 1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("materials_table", "Material 4"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("materials_table", "Material 3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("materials_table", "Material 4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("materials_table", "Material 5"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("materials_table", "Element Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("materials_table", "Isotopic\n"
"Abundance"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("materials_table", "Atomic Mass"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("materials_table", "Atomic Fraction"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("materials_table", "Density"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("materials_table", "Thickness"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("materials_table", "Component"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 3)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 4)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 5)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(1, 6)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 3)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 4)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 5)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(2, 6)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 3)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 4)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 5)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(3, 6)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 2)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 3)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 4)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 5)
        item.setText(_translate("materials_table", "0000"))
        item = self.tableWidget.item(4, 6)
        item.setText(_translate("materials_table", "0000"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    materials_table = QtWidgets.QWidget()
    ui = Ui_materials_table()
    ui.setupUi(materials_table)
    materials_table.show()
    sys.exit(app.exec_())
