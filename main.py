import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")

        res = self.connection.cursor().execute("""SELECT * FROM coffees""").fetchall()

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки',
                                                    'Форма', 'Описание вкуса', 'Цена', 'Объем упаковки'])

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    if elem:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str('молотый')))
                    else:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str('в зёрнах')))
                else:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())