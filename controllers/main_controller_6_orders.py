from model.manager_core import ManagerCore
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from controllers.main_controller import MainController
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QModelIndex, QObject, pyqtSlot
from controllers.main_controller import MainController
from controllers.new_order_controller import NewOrderController
from views.new_order_view import NewOrderView

class MainController_6_Orders(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui

        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._6_listView_finished_orders.setModel(self._list_model)

        # Connect slots/signals
        self._ui._6_listView_finished_orders.selectionModel().currentChanged.connect(self.on_listView_finished_orders_rowSelected)


    def update(self):
        # Get products
        ManagerCore().cursor.execute('''
            SELECT * FROM sales
        ''')
        
        # Fill Up list of products
        self._list_model.clear()
        self._id = 0

        for id, client_id in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {client_id}')
            self._list_model.appendRow(item)

        # Count of products
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM sales
        ''')
        self._ui._6_label_orders_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_finished_orders_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        req = ManagerCore().cursor.execute('''
            SELECT po.product_id, p.name, p.specs, p.price, po.count, c.fullname, c.id
                FROM product_orders AS po, products AS p, clients AS c, sales AS s
                WHERE s.id = ? AND c.id = s.cliend_id AND po.product_id = p.id AND po.sale_id = s.id
        ''').fetchall()[0]

        self._ui._6_label_product_id.setText(str(req[0]))
        self._ui._6_label_product_name.setText(str(req[1]))
        self._ui._6_plainTextEdit_product_specs.setPlainText(req[2])

        price = req[3]
        count = req[4]
        self._ui._6_label_price_for_one.setText(price)
        self._ui._6_label_count_of_product.setText(count)
        self._ui._6_label_price.setText(str(int(price) * int(count)))

        self._ui._6_plainTextEdit_client.setPlainText(req[5])


    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        ManagerCore().cursor.execute('''
            UPDATE clients
                SET fullname = ?,
                WHERE id = ?''', (self._ui._6_plainTextEdit_client.toPlainText(), int(req[6])))
        ManagerCore().db_connect.commit()
