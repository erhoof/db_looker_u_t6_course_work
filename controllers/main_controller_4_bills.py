from controllers.bills_report_controller import BillsReportController
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QModelIndex, QObject, pyqtSlot
from controllers.main_controller import MainController
from model.manager_core import ManagerCore
from views.bills_report_view import BillsReportView

class MainController_4_Bills(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui

        self._id = 0

        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._4_listView_bills.setModel(self._list_model)

        # Connect slots/signals
        self._ui._4_listView_bills.selectionModel().currentChanged.connect(self.on_listView_bills_rowSelected)


    def update(self):
        # Get manufacturers
        ManagerCore().cursor.execute('''
            SELECT id, type, price FROM payments
        ''')
        
        # Fill Up list of manufacturers
        self._list_model.clear()
        self._id = 0

        for id, type, price in ManagerCore().cursor:
            type = 'Со счета' if type else 'На счет'
            item = QStandardItem(f'({id}) :{type}: {price}')
            self._list_model.appendRow(item)

        # Count of manufacturers
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM payments
        ''')
        self._ui._4_label_bills_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_bills_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        # Get data
        ManagerCore().cursor.execute('''
            SELECT * FROM payments
                WHERE id = ?
        ''', [self._id])
        res = ManagerCore().cursor.fetchall()[0]

        # Get contract
        contract_id =ManagerCore().cursor.execute('''
            SELECT c.id FROM contracts AS c, product_orders AS po, payments AS p
                WHERE po.contract_id = c.id AND p.order_id = po.id
        ''').fetchall()[0][0]

        
        # Fill up with data
        self._ui._4_label_bill_id.setText(str(res[0]))
        self._ui._4_label_contract_id.setText(str(contract_id))
        self._ui._4_label_type.setText('Списание' if res[1] else 'Поступление')
        self._ui._4_lineEdit_sell_date.setText(res[3])
        self._ui._4_lineEdit_price.setText(res[4])
        self._ui._4_lineEdit_VAT.setText(res[5])
        self._ui._4_comboBox_pay.setCurrentIndex(res[6])
        self._ui._4_comboBox_income.setCurrentIndex(res[7])

        self.calculateVAT(res)

    
    def calculateVAT(self, res):
        vat = (1.0 + (0.01 * int(res[5]))) * float(res[4])
        self._ui._4_label_price_with_VAT.setText(str(vat))


    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        if not self._id: return

        date = self._ui._4_lineEdit_sell_date.text()
        price = self._ui._4_lineEdit_price.text()
        vat = self._ui._4_lineEdit_VAT.text()
        pay_status = self._ui._4_comboBox_pay.currentIndex()
        admission_status = self._ui._4_comboBox_income.currentIndex()

        if not date or not price or not vat:
            QMessageBox.warning('Ошибка ввода', 'Не все необходимые поля заполнены')
            return

        ManagerCore().cursor.execute('''
            UPDATE payments
                SET date = ?,
                    price = ?,
                    vat = ?,
                    payment_status = ?,
                    admission_status = ?
                WHERE id = ?''', (date, price, vat, pay_status, admission_status, self._id))
        ManagerCore().db_connect.commit()
        self.calculateVAT()
        QMessageBox.information(None, 'Изменение данных', 'Поля обновлены!')
        
    @pyqtSlot()
    def on_pushButton_about_bills_clicked(self):
        # Calculate full income / expenses

        income = 0.0
        expenses = 0.0

        data = ManagerCore().cursor.execute('SELECT type, price, vat FROM payments')
        for type, price, vat in ManagerCore().cursor:
            if type: # Expenses: price+VAT
                expenses += float(price)*(1 + 0.01*float(vat))
            elif not type: # Income: price-VAT
                income += float(price)*(1 - 0.01*float(vat))
            # case 2 does not included (not confirmed transaction)

        profit = income - expenses

        QMessageBox.information(None, 'Информация о счетах',
                                f'Доходы: {income}\nРасходы: {expenses}\nПрибыль: {profit}');


    @pyqtSlot()
    def on_pushButton_new_report_clicked(self):
        self._bills_report_controller = BillsReportController(None)
        self._bills_view = BillsReportView(self._bills_report_controller)
        self._bills_view.show()