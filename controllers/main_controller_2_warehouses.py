from PyQt5.QtWidgets import QInputDialog, QMessageBox
from model.manager_core import ManagerCore
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QModelIndex, QObject, pyqtSlot
from controllers.main_controller import MainController
from model.MEditProducts_model import EditMProductsTableModel

class MainController_2_Warehouses(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui
        self._id = 0

        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._2_listView_availWarehouse.setModel(self._list_model)

        # Connect slots/signals
        self._ui._2_listView_availWarehouse.selectionModel().currentChanged.connect(self.on_listView_availWarehouse_rowSelected)


    def update(self):
        # Get manufacturers
        ManagerCore().cursor.execute('''
            SELECT id, address FROM warehouses
        ''')
        
        # Fill Up list of manufacturers
        self._list_model.clear()
        self._id = 0

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_model.appendRow(item)

        # Count of manufacturers
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM warehouses
        ''')
        self._ui._2_label_warehouse_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')


    def update_products_table(self):
        if not self._id: return

        # Prepare table
        data = ManagerCore().cursor.execute('''
            SELECT * FROM products 
                WHERE id IN (SELECT product_id FROM product_orders
                                WHERE warehouse_id = ? AND remain_count>0)
        ''', str(self._id)).fetchall()
        self._table_model = EditMProductsTableModel(data)
        self._ui._2_tableView_products.setModel(self._table_model)


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_availWarehouse_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        # Get data
        ManagerCore().cursor.execute(f'''
            SELECT id, address
                FROM warehouses
                WHERE id={self._id}
        ''')
        res = ManagerCore().cursor.fetchall()[0]
        
        # Fill up with data
        self._ui._2_label_warehouse_id.setText(str(res[0]))
        self._ui._2_lineEdit_warehouse_address.setText(res[1])

        # Count
        data = ManagerCore().cursor.execute('''
            SELECT SUM(remain_count) FROM product_orders
                WHERE warehouse_id = ?
        ''', str(self._id)).fetchall()[0]
        self._ui._2_label_product_count.setText(str(data[0]) if data[0] else '0')

        # Price
        prices = ManagerCore().cursor.execute('''
            SELECT SUM(p.price*po.remain_count)
                FROM products AS p, product_orders AS po
                WHERE p.id IN
                    (SELECT product_id FROM product_orders
                        WHERE warehouse_id = ?)
                AND p.id = po.product_id
        ''', str(self._id)).fetchall()[0]
        self._ui._2_label_full_price.setText(str(prices[0]) if prices[0] else '0')

        self.update_products_table()

    
    @pyqtSlot()
    def on_pushbutton_new_warehouse_clicked(self):
        addr = QInputDialog.getText(None, 'Создание склада', 'Введите адрес склада:')
        if not addr[1] or not addr[0]: return

        ManagerCore().cursor.execute('INSERT INTO warehouses(address) VALUES (?)', [addr[0]])
        ManagerCore().db_connect.commit()
        self.update()


    @pyqtSlot()
    def on_pushButton_remove_clicked(self):
        reply = QMessageBox.warning(None, 'Удаление склада',
         '''При удалении склада товары с него будут
         перемещены на следующий доступный.''',
          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.No: return

        data = ManagerCore().cursor.execute(
            'SELECT warehouse_id FROM product_orders WHERE warehouse_id != ?',
            str(self._id)).fetchall()

        print(data)
            
        if not len(data):
            reply = QMessageBox.warning(None, 'Удаление склада',
            'Нет доступных складов! Удаление склада повлечет удаление заказов, вы уверены?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
            if reply == QMessageBox.No: return

            # 1. Remove contracts
            ManagerCore().cursor.execute('''
                DELETE FROM contracts WHERE id IN 
                    (SELECT contract_id FROM product_orders WHERE warehouse_id = ?)''', [self._id])

            # 2. Remove sales
            ManagerCore().cursor.execute('''
                DELETE FROM sales WHERE product_order_id IN 
                    (SELECT sale_id FROM product_orders WHERE warehouse_id = ?)''', [self._id])

            # 3. Remove payments
            ManagerCore().cursor.execute('''
                DELETE FROM payments WHERE order_id IN 
                    (SELECT id FROM product_orders WHERE warehouse_id = ?)''', [self._id])

            # 4. Remove product order
            ManagerCore().cursor.execute('DELETE FROM product_orders WHERE warehouse_id = ?', [self._id])

            # 5. Remove warehouse
            ManagerCore().cursor.execute('DELETE FROM warehouses WHERE id = ?', [self._id])

            ManagerCore().db_connect.commit()

        # Warehouses list
        req = ManagerCore().cursor.execute('SELECT * FROM warehouses').fetchall()
        req_map = {id: addr for id, addr in req}
        item, ok = QInputDialog.getItem(None,
             'Удаление склада',
             'Выберите склад для перемещения',
             (f'{key}:{val}'for key, val in req_map), 0, False)

        if not ok: return

        QMessageBox.information(None, 'Удаление склада', f'Переезжаем в {item}')
        newId = item[:item.find(':')]
        
        # 1. Move to new warehouse
        ManagerCore().cursor.execute('''
            UPDATE product_orders
                SET warehouse_id = ?,
                WHERE warehouse_id = ?''', (int(newId), int(self._id)))

        # 2. Remove warehouse
        ManagerCore().cursor.execute('DELETE FROM warehouses WHERE id = ?', [self._id])
        ManagerCore().db_connect.commit()

    
    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        if self._id == 0: return

        addr = self._ui._2_lineEdit_warehouse_address.text()

        if not addr: return

        ManagerCore().cursor.execute('''
            UPDATE warehouses
                SET address = ?
                WHERE id = ?''', (addr, int(self._id)))
        
        QMessageBox.information(None, 'Изменение данных', 'Поля обновлены!')

