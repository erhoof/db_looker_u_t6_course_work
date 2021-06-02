from PyQt5.QtGui import QStandardItem, QStandardItemModel
from views.gen.ui_new_order_view import Ui_NewOrderView
from model.manager_core import ManagerCore
from PyQt5.QtCore import QModelIndex, QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox
import logging

class NewOrderController(QObject):

    def __init__(self, ui: Ui_NewOrderView = None):
        super().__init__()
        self._ui = ui
        self._product_name = ''


    def update(self):
        # Setup UI
        self._ui.listView_products.setEnabled(False)
        self._ui.pushButton_add_product.setEnabled(False)
        self._ui.spinBox_count.setEnabled(False)
        self._ui.pushButton_remove.setEnabled(False)

        # Fill Up Warehouses
        # Warehouses list
        self._warehouses = ManagerCore().cursor.execute('SELECT * FROM warehouses').fetchall()
        self._warehouses_map = {id: addr for id, addr in self._warehouses}
        if not self._warehouses[0][0]:
            QMessageBox.warning('Ошибка создания контракта', 'Невозможно создать контракт, не имея доступных складов')
            self._view.close()
        
        for name in self._warehouses_map.values():
            self._ui.comboBox_warehouses.addItem(name)


        # Setup manufacturers
        self._list_manufacturer_model = QStandardItemModel()
        self._ui.listView_manufacturers.setModel(self._list_manufacturer_model)

        ManagerCore().cursor.execute('''
            SELECT id, name FROM manufacturers
        ''')
        
        # Fill Up list of manufacturers
        self._m_id = 0
        self._product_id = 0

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_manufacturer_model.appendRow(item)


    def calculatePrice(self):
        full_price = 0.0

        for row in range(self._list_order_model.rowCount(self._ui.listView_selected.rootIndex())):
            child_index = self._list_order_model.index(row, 0, self._ui.listView_selected.rootIndex())
            data = str(self._list_order_model.data(child_index))

            id = data[data.find('(')+1: data.find(')')]
            count = data[data.find('-')+2:]

            # Get Price
            price = ManagerCore().cursor.execute('SELECT price FROM products WHERE id = ?', [int(id)]).fetchall()[0][0]

            full_price += float(count) * float(price)

        self._ui.label_full_price.setText(str(full_price))


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_manufactures_rowSelected(self, selected: QModelIndex):
        string = str(self._list_manufacturer_model.data(selected))
        self._m_id = string[string.find('(')+1: string.find(')')]

        # Setup manufacturers
        self._list_products_model = QStandardItemModel()
        self._ui.listView_products.setModel(self._list_products_model)

        ManagerCore().cursor.execute('''
            SELECT id, name FROM products WHERE manufacturer_id = ?
        ''', [self._m_id])

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_products_model.appendRow(item)


    @pyqtSlot()
    def on_pushButton_add_manufacturer_clicked(self):
        # Lock manufacturer
        self._ui.listView_products.setEnabled(True)
        self._ui.listView_manufacturers.setEnabled(False)
        self._ui.pushButton_add_manufacturer.setEnabled(False)
        self._ui.pushButton_add_product.setEnabled(True)

        # Setup manufacturers
        self._list_order_model = QStandardItemModel()
        self._ui.listView_selected.setModel(self._list_order_model)
        self._ui.listView_products.selectionModel().currentChanged.connect(self.on_listView_products_rowSelected)
        self._ui.listView_selected.selectionModel().currentChanged.connect(self.on_listView_selected_rowSelected)

        # Select product
        string = str(self._list_products_model.data(self._list_products_model.index(0, 0)))
        self._product_id = string[string.find('(')+1: string.find(')')]
        self._product_name = string[string.find(')')+2:]


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_products_rowSelected(self, selected: QModelIndex):
        string = str(self._list_products_model.data(selected))
        self._product_id = string[string.find('(')+1: string.find(')')]
        self._product_name = string[string.find(')')+2:]


    @pyqtSlot()
    def on_pushButton_add_product_clicked(self):
        if not self._product_name: return

        item = QStandardItem(f'({self._product_id}) {self._product_name} - 1')
        #TODO: Check for unique
        self._list_order_model.appendRow(item)
        self.calculatePrice()


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_selected_rowSelected(self, selected: QModelIndex):
        string = str(self._list_order_model.data(selected))
        count = string[string.find('-')+2:]
        self._selected_id = string[string.find('(')+1: string.find(')')]
        self._selected_index = selected

        print('count:', string)
        self._ui.spinBox_count.setValue(int(count))
        self._ui.spinBox_count.setEnabled(True)


    @pyqtSlot(int)
    def on_spinbox_count_valueChanged(self, index):
        string = str(self._list_order_model.data(self._selected_index))
        string_wo_count = string[:string.find('-')+1]
        full_string = f'{string_wo_count} {index}'
        print(full_string)
        
        self._list_order_model.setData(self._selected_index, full_string)
        self.calculatePrice()


    @pyqtSlot()
    def on_pushButton_remove_clicked(self):
        self._list_products_model.removeRow(self._selected_index.row())

        self._ui.spinBox_count.setEnabled(False)
        self._ui.pushButton_remove.setEnabled(False)


    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self._view.close()


    @pyqtSlot()
    def on_pushButton_make_a_deal_clicked(self):
        concluson_date = self._ui.dateEdit_conclusion.text()
        delivery_date = self._ui.dateEdit_delivery.text()

        # 1. Generate Contract
        ManagerCore().cursor.execute('''
            INSERT INTO contracts 
                (manufacturer_id, conclusion_date, delivery_date, delivery_conditions)
                VALUES (?, ?, ?, ?)
        ''', (int(self._m_id), concluson_date, delivery_date, self._ui.lineEdit_conditions.text()))
        ManagerCore().db_connect.commit()
        contract_id = ManagerCore().cursor.execute('SELECT last_insert_rowid()').fetchall()[0][0]

        # Get warehouse ID
        warehouse_id = list(self._warehouses_map.keys())[self._ui.comboBox_warehouses.currentIndex()]

        for row in range(self._list_order_model.rowCount(self._ui.listView_selected.rootIndex())):
            child_index = self._list_order_model.index(row, 0, self._ui.listView_selected.rootIndex())
            data = str(self._list_order_model.data(child_index))

            id = data[data.find('(')+1: data.find(')')]
            count = data[data.find('-')+2:]

            # Get Price
            price = ManagerCore().cursor.execute('SELECT price FROM products WHERE id = ?', [int(id)]).fetchall()[0][0]
            full_price = float(price) * float(count)

            # 2. Generate order
            ManagerCore().cursor.execute('''
                INSERT INTO product_orders 
                    (contract_id, product_id, count, remain_count, warehouse_id)
                    VALUES (?, ?, ?, ?, ?)
            ''', (int(contract_id), int(id), int(count), int(count), int(warehouse_id)))
            ManagerCore().db_connect.commit()
            order_id = ManagerCore().cursor.execute('SELECT last_insert_rowid()').fetchall()[0][0]

            # 3. Generate payment for order
            ManagerCore().cursor.execute('''
                INSERT INTO payments 
                    (type, order_id, date, price, vat, payment_status, admission_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (1, order_id, concluson_date, full_price, '20', 0, 0))
            ManagerCore().db_connect.commit()
        
        self._view.close()
        


        
            

        
