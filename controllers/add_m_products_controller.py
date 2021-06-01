from PyQt5.QtWidgets import QMessageBox
from model.MEditProducts_model import EditMProductsTableModel
from views.gen.ui_m_add_products_view import Ui_m_add_products_view
from PyQt5.QtCore import QItemSelection, QObject, pyqtSlot, Qt
from model.manager_core import ManagerCore
import logging

class AddMProductsController(QObject):

    def __init__(self, manufacturer_id, ui: Ui_m_add_products_view = None):
        super().__init__()
        self._ui = ui
        self._manufacturer_id = manufacturer_id
        self._id = 0


    def update(self):
        self._view.setWindowTitle(f'Редактирование Товара (mID: {self._manufacturer_id})')

        # Prepare table
        self._table_model = EditMProductsTableModel(self.getData())
        self._ui.tableView_products.setModel(self._table_model)
        self.updateTable()


    def getData(self):
        print(self._manufacturer_id)
        ManagerCore().cursor.execute('''
            SELECT * FROM products WHERE manufacturer_id=?
        ''', str(self._manufacturer_id))
        return ManagerCore().cursor.fetchall()


    def updateTable(self):
        self._ui.tableView_products.update()


    @pyqtSlot()
    def on_pushButton_add_clicked(self):
        name = self._ui.lineEdit_name.text()
        specs = self._ui.plainTextEdit_specs.toPlainText()
        price = self._ui.lineEdit_price.text()
        packaging = self._ui.lineEdit_packaging.text()
        addon = self._ui.lineEdit_addon.text()

        if not name or not specs or not price:
            QMessageBox.warning('Ошибка ввода', 'Не все необходимые поля заполнены')
            return

        ManagerCore().cursor.execute('''
            INSERT INTO products(manufacturer_id, name, specs, price, packaging, addon) VALUES(?, ?, ?, ?, ?, ?)
        ''', (self._manufacturer_id, name, specs, price, packaging, addon))
        ManagerCore().db_connect.commit()
        #TODO: remove this dirty hack
        self.update()


    @pyqtSlot(QItemSelection, QItemSelection)
    def on_table_cell_clicked(self, selected: QItemSelection):
        row = 0
        try:
            row = selected.first().indexes()[0].row()
        except:
            logging.warn('pyqt tablecell selected range error')
            return

        self._id = self._table_model.data(self._table_model.index(row, 0), Qt.DisplayRole)
        # Get data
        ManagerCore().cursor.execute(f'''
            SELECT id, manufacturer_id, name, specs, price, packaging, addon 
                FROM products
                WHERE manufacturer_id={self._manufacturer_id} 
                    AND id={self._id} 
        ''')
        res = ManagerCore().cursor.fetchall()[0]
        
        # Fill up with data
        self._ui.label_9.setText(str(res[0]))
        self._ui.lineEdit_name.setText(res[2])
        self._ui.plainTextEdit_specs.setPlainText(res[3])
        self._ui.lineEdit_price.setText(res[4])
        self._ui.lineEdit_packaging.setText(res[5])
        self._ui.lineEdit_addon.setText(res[6])


    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        if self._id == 0: return

        id = self._ui.label_9.text()
        name = self._ui.lineEdit_name.text()
        specs = self._ui.plainTextEdit_specs.toPlainText()
        price = self._ui.lineEdit_price.text()
        packaging = self._ui.lineEdit_packaging.text()
        addon = self._ui.lineEdit_addon.text()

        if not name or not specs or not price:
            QMessageBox.warning('Ошибка ввода', 'Не все необходимые поля заполнены')
            return

        print('mi:', int(self._manufacturer_id))
        print('id:', int(self._id))
        ManagerCore().cursor.execute(f'''
            UPDATE products
                SET name = ?,
                    specs = ?,
                    price = ?,
                    packaging = ?,
                    addon = ?
                WHERE manufacturer_id = ? AND id = ?''',
                (name, specs, price, packaging, addon, int(self._manufacturer_id), int(self._id)))
        ManagerCore().db_connect.commit()
        self.update()

    
    @pyqtSlot()
    def on_pushButton_remove_clicked(self):
        if self._id == 0: return

        id = self._ui.label_9.text()
        ManagerCore().cursor.execute('DELETE FROM products WHERE id = ?', id)
        ManagerCore().db_connect.commit()
        self.update()



