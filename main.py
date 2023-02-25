import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QButtonGroup


class AddEdit(QWidget):
    def __init__(self, con, update_table, to_edit=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = con
        self.to_edit = to_edit
        self.update_table = update_table
        self.states = QButtonGroup()
        self.states.addButton(self.state_0)
        self.states.addButton(self.state_1)

        if to_edit:
            self.add_edit_btn.clicked.connect(self.edit_coffee)
            self.setWindowTitle('Изменение вида кофе')
            self.add_edit_btn.setText('Изменить')
            self.name.setText(to_edit[1])
            self.degree.setText(to_edit[2])
            if to_edit[3]:
                self.state_0.setChecked(1)
                self.state_1.setChecked(0)
            else:
                self.state_0.setChecked(0)
                self.state_1.setChecked(1)
            self.description.setText(to_edit[4])
            self.price.setValue(int(to_edit[5]))
            self.size.setValue(int(to_edit[6]))
        else:
            self.add_edit_btn.clicked.connect(self.add_coffee)

    def edit_coffee(self):
        self.modified = {}

        try:
            if self.name.text() != self.to_edit[1]:
                self.modified['name'] = self.name.text()
            if self.degree.text() != self.to_edit[2]:
                self.modified['degree'] = self.degree.text()
            if self.state_0.isChecked() != self.to_edit[3]:
                self.modified['is_ground'] = self.state_0.isChecked()
            if self.description.toPlainText() != self.to_edit[4]:
                self.modified['description'] = self.description.toPlainText()
            if self.price.value() != self.to_edit[5]:
                self.modified['price'] = int(self.price.value())
            if self.size.value() != self.to_edit[6]:
                self.modified['size'] = int(self.size.value())
        except Exception:
            self.error.setText('Неверно заполнена форма')
            return
        if self.modified:
            self.error.setText('')
            cur = self.con.cursor()
            que = "UPDATE coffees SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.to_edit[0],))
            self.con.commit()
            self.update_table()
            self.close()
        else:
            self.error.setText('Ничего не изменилось')

    def add_coffee(self):
        self.modified = {}
        try:
            self.modified['name'] = self.name.text()
            self.modified['degree'] = self.degree.text()
            self.modified['is_ground'] = int(self.state_0.isChecked())
            self.modified['description'] = self.description.toPlainText()
            self.modified['price'] = self.price.value()
            self.modified['size'] = self.size.value()
        except Exception:
            self.error.setText('Неверно заполнена форма')
            return

        self.error.setText('')
        cur = self.con.cursor()
        que = "INSERT INTO coffees (name, degree, is_ground, description, price, size) VALUES ("
        que += ", ".join([f"'{self.modified.get(key)}'" for key in self.modified.keys()])
        cur.execute(que + ')')
        self.con.commit()
        self.update_table()
        self.close()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.update_table()
        self.add_btn.clicked.connect(self.open_add)
        self.edit_btn.clicked.connect(self.open_edit)

    def update_table(self):
        res = self.connection.cursor().execute("""SELECT * FROM coffees""").fetchall()

        self.tableWidget.setColumnCount(7)
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

    def find_selected(self):
        return [self.tableWidget.item(list(set([j.row() for j in self.tableWidget.selectedItems()]))[0], i).text()
                for i in range(7)]

    def open_add(self):
        self.form = AddEdit(self.connection, self.update_table)
        self.form.show()

    def open_edit(self):
        if self.tableWidget.selectedItems():
            self.form = AddEdit(self.connection, self.update_table, self.find_selected())
            self.form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
