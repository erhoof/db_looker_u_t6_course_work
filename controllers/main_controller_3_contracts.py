from model.MEditProducts_model import EditMProductsTableModel
from PyQt5.QtWidgets import QMessageBox
from model.manager_core import ManagerCore
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from views.new_order_view import NewOrderView
from controllers.new_order_controller import NewOrderController
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QModelIndex, QObject, pyqtSlot, QDate
from controllers.main_controller import MainController

class MainController_3_Contracts(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui

        self._id = 0
        print(self)

        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._3_listView_contracts.setModel(self._list_model)

        # Connect slots/signals
        self._ui._3_listView_contracts.selectionModel().currentChanged.connect(self.on_listView_contracts_rowSelected)


    def update(self):
        # Get contracts
        ManagerCore().cursor.execute('''
            SELECT c.id, m.name 
                FROM contracts AS c, manufacturers AS m
                WHERE c.manufacturer_id = m.id
        ''')
        
        # Fill Up list of manufacturers
        self._list_model.clear()
        self._id = 0

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_model.appendRow(item)

        # Count of manufacturers
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM contracts
        ''')
        self._ui._3_label_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')


    def update_products_table(self):
        if not self._id: return

        # Prepare table
        data = ManagerCore().cursor.execute('''
            SELECT * FROM products WHERE id IN
                (SELECT product_id FROM product_orders WHERE contract_id = ?)
        ''', [int(self._id)]).fetchall()
        self._table_model = EditMProductsTableModel(data)
        self._ui._3_tableView_products.setModel(self._table_model)


    def calculatePrice(self):
        full_price = 0.0

        data = ManagerCore().cursor.execute('''
            SELECT SUM(p.price*po.count)
                FROM products AS p, product_orders AS po
                WHERE p.id IN
                    (SELECT product_id FROM product_orders
                        WHERE contract_id = ?)
                AND p.id = po.product_id
        ''', [self._id])

        for sum in ManagerCore().cursor:
            full_price += float(sum[0])

        self._ui._3_label_price.setText(str(full_price))


    @pyqtSlot()
    def on_pushButton_newContract_clicked(self):
        self._new_order_controller = NewOrderController()
        self._new_order_view = NewOrderView(self._new_order_controller)
        self._new_order_view.show()


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_contracts_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        # Get data
        ManagerCore().cursor.execute(f'''
            SELECT * FROM contracts
                WHERE id={self._id}
        ''')
        res = ManagerCore().cursor.fetchall()[0]

        self._ui._3_label_idContract.setText(str(res[0]))
        self._ui._3_label_idManufacturer.setText(str(res[1]))
        self._ui._3_dateEdit_conclusion.setDate(QDate.fromString(res[2], 'yyyy-MM-dd'))
        self._ui._3_dateEdit_delivery.setDate(QDate.fromString(res[3], 'yyyy-MM-dd'))
        self._ui._3_lineEdit_delivery_conditions.setText(res[4])
        self.calculatePrice()
        self.update_products_table()


    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        date_conclusion = self._ui._3_dateEdit_conclusion.text()
        date_delivery = self._ui._3_dateEdit_delivery.text()
        delivery_conditions = self._ui._3_lineEdit_delivery_conditions.text()

        ManagerCore().cursor.execute('''
            UPDATE contracts
                SET conclusion_date = ?,
                    delivery_date = ?,
                    delivery_conditions = ?
                WHERE id = ?''', (date_conclusion, date_delivery, delivery_conditions, self._id))
        ManagerCore().db_connect.commit()


    @pyqtSlot()
    def on_pushButton_remove_clicked(self):
        if not self._id: return
        
        reply = QMessageBox.warning(None, 'Удаление договора',
         '''При удалении договора, все имеющиеся 
         по нему товары и счета будут удалены. Продолжить?''',
          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.No: return

        # 1. Delete payments
        ManagerCore().cursor.execute('''
            DELETE FROM payments WHERE order_id IN 
                (SELECT id FROM product_orders WHERE contract_id = ?)''', self._id)

        # 2. Delete orders
        ManagerCore().cursor.execute('DELETE FROM product_orders WHERE contract_id = ?', self._id)

        # 3. Delete contract
        ManagerCore().cursor.execute('DELETE FROM contracts WHERE id = ?', self._id)
        ManagerCore().db_connect.commit()

        self._id = 0
        self._ui._3_label_idContract.setText('0')
        self.update()


