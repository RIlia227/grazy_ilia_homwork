import sqlite3
import sys

from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5 import uic

con = sqlite3.connect("coffee.db")
cur = con.cursor()

class MyWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.table = []
        self.head = ["ID", "сорт", "степень обжарки", "молотый или нет", "вкус", "цена", "обём"]
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.obnov.clicked.connect(self.update_table)
        self.add.clicked.connect(self.add_function)
        self.update_table()

    def add_function(self):
        self.op = Window2(self)
        self.op.show()

    def update_table(self):
        self.table = self.get_table()
        self.tableWidget.setColumnCount(len(self.table[0]))
        self.tableWidget.setRowCount(len(self.table))
        self.tableWidget.setHorizontalHeaderLabels([i for i in self.head])
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.resizeColumnToContents(3)
        print(self.table)
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                if j == 2:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.select_obj(i, j)[0][0]))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.table[i][j])))

    def select_obj(self, i, j):
        print(self.table[i][j])
        result = cur.execute("SELECT title FROM stepeni_proj WHERE id=?",
                             (item_year := self.table[i][j], )).fetchall()
        return result

    def get_table(self):
        result = cur.execute("SELECT * FROM coffees").fetchall()
        return result

class Window2(QDialog):
    def __init__(self, *args):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.combo()
        self.add_2.clicked.connect(self.new_item)
        self.comboBox.activated[str].connect(self.onChanged)
        self.del_id = 0

    def onChanged(self, text):
        result = cur.execute(f"SELECT * FROM coffees WHERE ID={text}").fetchall()
        self.ID.setText(str(result[0][0]))
        self.sort_name.setText(str(result[0][1]))
        self.step_objarki.setText(str(result[0][2]))
        self.molot_or_not.setText(str(result[0][3]))
        self.taste.setText(str(result[0][4]))
        self.coste.setText(str(result[0][5]))
        self.amount.setText(str(result[0][6]))
        self.del_id = text
        print(result)

    def combo(self):
        result = cur.execute(f"SELECT ID FROM coffees").fetchall()
        result = [i[0] for i in result]
        for i in result:
            self.comboBox.addItem(str(i))

    def new_item(self):
        self.err = []
        ID = self.ID.text()
        sort_name = str(self.sort_name.text())
        step_objarki = self.step_objarki.text()
        molot_or_not = str(self.molot_or_not.text())
        taste = str(self.taste.text())
        coste = self.coste.text()
        amount = self.amount.text()
        sp = [ID, sort_name, step_objarki, molot_or_not, taste, coste, amount]
        if '' not in sp:
            if self.del_id != 0:
                cur.execute(f"DELETE from coffees WHERE id={self.del_id}")
            cur.execute(f"INSERT INTO coffees(ID, sort_name, step_objarki, molot_or_not, taste, coste, amount)"
                        f"VALUES ({ID}, '{sort_name}', {step_objarki}, '{molot_or_not}', '{taste}', {coste}, {amount})")
            self.error.setText("Элемент создан.")
            self.close()
        else:
            self.error.setText("Элемент не создан из-за ошибок в параметрах.")
        con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())