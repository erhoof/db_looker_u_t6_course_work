from controllers.main_controller import MainController
from views.gen.ui_new_sale_view import Ui_new_sale_view
from model.manager_core import ManagerCore
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
import logging

class NewSaleController(QObject):

    def __init__(self, product_id, ui: Ui_new_sale_view = None):
        super().__init__()
        self._ui = ui
        self._id = product_id


    def update(self):
        # Get product name
        ManagerCore().cursor.execute(f'''
            SELECT p.name, m.name FROM products AS p, manufacturers AS m
                WHERE p.manufacturer_id = m.id AND p.id = ?
        ''', [self._id])
        res = ManagerCore().cursor.fetchall()[0]

        self._ui.label_name.setText(res[0])
        self._ui.label_manufacturer.setText(res[1])

        # Get warehouses
        self._ui.comboBox_warehouse.clear()
        ManagerCore().cursor.execute(f'''
            SELECT po.id, w.id, w.address, po.remain_count FROM warehouses AS w, product_orders AS po
                WHERE w.id IN (
                    SELECT warehouse_id FROM product_orders WHERE product_id = ?
                ) AND po.product_id = ? AND po.warehouse_id = w.id AND po.contract_id IS NOT NULL
        ''', (self._id, self._id))
        self._product_orders_dict = dict() # for decreasing numb war
        for po_id, id, address, count in ManagerCore().cursor:
            self._ui.comboBox_warehouse.addItem(f'{id} - {address} ({count}шт.)')
            self._product_orders_dict[id] = po_id

        self.setPriceText()


    def calculatePrice(self):
        count = self._ui.spinBox.value()
        price = ManagerCore().cursor.execute('SELECT price FROM products WHERE id = ?', [self._id]).fetchall()[0][0]

        return float(count) * float(price)


    def setPriceText(self):
        self._ui.label_8.setText(
        f'''Цена (без НДС): {str(self.calculatePrice())}
        НДС: 20%
        --------
        Итого: {str(self.calculatePrice() * 1.2)}
        ''')


    @pyqtSlot(int)
    def on_spinBox_currentValue_changed(self):
        self.setPriceText()


    @pyqtSlot()
    def on_pushButton_clicked(self):
        # Check if out of bounds
        string = self._ui.comboBox_warehouse.currentText()
        max_count = string[string.find('(')+1 : string.find(')') - 3]
        warehouse_id = string[:string.find('-')-1]

        if self._ui.spinBox.value() > int(max_count):
            QMessageBox.warning(None, 'Ошибка ввода', 'На этом складе нет столько товара')
            return

        # 1. Create Client / Check if exists
        client_id = ManagerCore().cursor.execute('''
            SELECT id FROM clients WHERE fullname = ? 
        ''', [self._ui.lineEdit_client.text()]).fetchall()
        print('CLIENT_ID:', client_id)
        if not client_id:
            # Creating new client
            ManagerCore().cursor.execute('''
                INSERT INTO clients (fullname) VALUES (?)
            ''', [self._ui.lineEdit_client.text()]).fetchall()
            ManagerCore().db_connect.commit()
            client_id = ManagerCore().cursor.execute('SELECT last_insert_rowid()').fetchall()[0][0]
        else:
            client_id = client_id[0][0]

        print(client_id)
        # 2. Create Sale
        ManagerCore().cursor.execute('''
            INSERT INTO sales (client_id) VALUES (?)
        ''', [int(client_id)]).fetchall()
        ManagerCore().db_connect.commit()
        sale_id = ManagerCore().cursor.execute('SELECT last_insert_rowid()').fetchall()[0][0]

        # 3. Create order
        ManagerCore().cursor.execute('''
            INSERT INTO product_orders 
                (sale_id, product_id, count, warehouse_id)
                VALUES (?, ?, ?, ?)
        ''', (int(sale_id), int(self._id), self._ui.spinBox.value(), int(warehouse_id)))
        ManagerCore().db_connect.commit()
        order_id = ManagerCore().cursor.execute('SELECT last_insert_rowid()').fetchall()[0][0]

        # 4. Create payment
        ManagerCore().cursor.execute('''
            INSERT INTO payments 
                (type, order_id, date, price, vat, payment_status, admission_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (1, int(order_id), self._ui.dateEdit.text(), str(self.calculatePrice()), '20', 0, 0))
        ManagerCore().db_connect.commit()

        # 5. Decrease remaining count
        remain_count = int(int(max_count) - self._ui.spinBox.value())
        ManagerCore().cursor.execute(f'''
            UPDATE product_orders
                SET remain_count = ?
                    WHERE id = ?''',
                (remain_count, int(self._product_orders_dict[int(warehouse_id)])))
        ManagerCore().db_connect.commit()

        QMessageBox.information(None, 'Успешная продажа!', f'''
            Заказ №: {str(order_id)}
            Выдача по адресу: {self._ui.comboBox_warehouse.currentText()}
            --------------------------------------
            Наименование: {self._ui.label_name.text()}
            Производитель: {self._ui.label_manufacturer.text()}
            Кол-во: {self._ui.spinBox.value()} шт.
            --------------------------------------
            Расчет (без НДС): {self.calculatePrice()}
            НДС: 20%

            Итого: {self.calculatePrice() * 1.2}  
        ''')
        self._view.close()

        


    
    

    

        


        
            

        
