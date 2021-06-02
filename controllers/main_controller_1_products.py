from model.manager_core import ManagerCore
from PyQt5.QtCore import QModelIndex, pyqtSlot
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from controllers.main_controller import MainController
from model.manager_core import ManagerCore
import sqlite3

class MainController_1_Products(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui
        
        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._1_listView_avail.setModel(self._list_model)

        # Connect slots/signals
        self._ui._1_listView_avail.selectionModel().currentChanged.connect(self.on_listView_avail_rowSelected)


    def update(self):
        # Get products
        ManagerCore().cursor.execute('''
            SELECT id, name FROM products
                WHERE id IN (SELECT product_id FROM product_orders WHERE remain_count > 0)
        ''')
        
        # Fill Up list of products
        self._list_model.clear()
        self._id = 0

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_model.appendRow(item)

        # Count of products
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM products
                WHERE id IN (SELECT product_id FROM product_orders WHERE remain_count > 0)
        ''')
        self._ui._1_label_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_avail_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        # Get data
        ManagerCore().cursor.execute(f'''
            SELECT *  FROM products
                WHERE id = ?
        ''', [self._id])
        res = ManagerCore().cursor.fetchall()[0]
        # Get manufacturer name
        ManagerCore().cursor.execute(f'''
            SELECT name FROM manufacturers
                WHERE id = ?
        ''', [int(res[1])])
        manufacturer_name = ManagerCore().cursor.fetchall()[0][0]
        # Get remain count
        ManagerCore().cursor.execute(f'''
            SELECT SUM(remain_count) FROM product_orders WHERE product_id = ?
        ''', [int(self._id)])
        remain_count = ManagerCore().cursor.fetchall()[0][0]


        self._ui._1_label_id_product.setText(str(res[0]))
        self._ui._1_label_name.setText(res[2])
        self._ui._1_manufacturer_name.setText(manufacturer_name)
        self._ui._1_plainTextEdit_specs.setPlainText(res[3])
        self._ui._1_label_price.setText(res[4])
        self._ui._1_label_packaging.setText(res[5])
        self._ui._1_plainTextEdit_addon.setPlainText(res[6])
        self._ui._1_label_product_count.setText(str(remain_count))

        # Get warehouses
        self._ui._1_comboBox_avail.clear()
        ManagerCore().cursor.execute(f'''
            SELECT w.id, w.address, po.remain_count FROM warehouses AS w, product_orders AS po
                WHERE w.id IN (
                    SELECT warehouse_id FROM product_orders WHERE product_id = ?
                ) AND po.product_id = ? AND po.warehouse_id = w.id
        ''', (self._id, self._id))
        for id, address, count in ManagerCore().cursor:
            self._ui._1_comboBox_avail.addItem(f'{id} - {address} ({count}шт.)')