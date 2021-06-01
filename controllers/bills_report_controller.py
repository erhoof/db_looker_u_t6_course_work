from PyQt5.QtWidgets import QMessageBox
from model.MEditProducts_model import EditMProductsTableModel
from views.gen.ui_bills_report_view import Ui_bills_report_view
from PyQt5.QtCore import QItemSelection, QObject, pyqtSlot, Qt
from model.manager_core import ManagerCore
import logging
from model.bills_report_table_model import BillsReportTableModel

class BillsReportController(QObject):

    def __init__(self, ui: Ui_bills_report_view = None):
        super().__init__()
        self._ui = ui


    def update_products_table(self):
        # Prepare table
        pass
        #data = ManagerCore().cursor.execute('''
        #    SELECT * FROM products WHERE manufacturer_id=?
        #''', str(self._id)).fetchall()
        #self._table_model = EditMProductsTableModel(data)
        #self._ui._5_tableView_products.setModel(self._table_model)


    def prepareTable(self, start, end, type):
        data = ManagerCore().cursor.execute('''
            SELECT pay.id, pr.name, ord.count, pay.price, pay.vat
                FROM payments AS pay, product_orders AS ord, products AS pr
                WHERE pay.order_id = ord.id AND ord.product_id = pr.id AND pay.type = ? AND pay.date BETWEEN ? AND ?
        ''', (int(type), start, end)).fetchall()
        
        # Prepare table
        self._table_model = BillsReportTableModel(data)
        self._ui.tableView.setModel(self._table_model)

        return data


    def expenses(self, start, end):
        data = self.prepareData(start, end, 1)


    def income(self, start, end):
        pass


    @pyqtSlot()
    def on_pushButton_create_clicked(self):
        start_date = self._ui.dateEdit_begin.text()
        end_date = self._ui.dateEdit_end.text()

        type = self._ui.comboBox_type.currentIndex()
        data = ManagerCore().cursor.execute('SELECT price, vat FROM payments WHERE type = ?', [int(type)])
        count = ManagerCore().cursor.execute('SELECT COUNT(price) FROM payments WHERE type = ?', [int(type)]).fetchall()[0][0]
        report = ''

        if type: # Expenses
            expenses = 0.0

            for price, vat in ManagerCore().cursor:
                expenses += float(price)*(1 + 0.01*float(vat))

            report = f'Суммарно расходов:\n  {str(expenses)}\n\nКол-во:\n  {str(count if count else 0)}'

        else: # Income
            income = 0.0

            for price, vat in ManagerCore().cursor:
                income += float(price)*(1 - 0.01*float(vat))

            report = f'Суммарно доходов:\n  {str(income)}\n\nКол-во:\n  {str(count if count else 0)}'

        self._ui.plainTextEdit_result.setPlainText(report)

        self.prepareTable(start_date, end_date, type)
            
