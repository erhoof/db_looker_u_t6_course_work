from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

from views.gen.ui_main_view import Ui_MainWindow

from controllers.main_controller import MainController
from controllers.main_controller_1_products import MainController_1_Products
from controllers.main_controller_2_warehouses import MainController_2_Warehouses
from controllers.main_controller_3_contracts import MainController_3_Contracts
from controllers.main_controller_4_bills import MainController_4_Bills
from controllers.main_controller_5_manufacturers import MainController_5_Manufacturers
from controllers.main_controller_6_orders import MainController_6_Orders

class MainView(QMainWindow):
    def __init__(self, controller: MainController):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._controller = controller
        self._controller._ui = self._ui
        self._controller._1_products_tab = MainController_1_Products(self._controller)
        self._controller._2_warehouses_tab = MainController_2_Warehouses(self._controller)
        self._controller._3_contracts_tab = MainController_3_Contracts(self._controller)
        self._controller._4_bills_tab = MainController_4_Bills(self._controller)
        self._controller._5_manufacturers_tab = MainController_5_Manufacturers(self._controller)
        self._controller._6_orders_tab = MainController_6_Orders(self._controller)

        # Tab Buttons
        self._ui.pushButton_products.clicked.connect(self._controller.on_pushButton_products_clicked)
        self._ui.pushButton_warehouses.clicked.connect(self._controller.on_pushButton_warehouses_clicked)
        self._ui.pushButton_contracts.clicked.connect(self._controller.on_pushButton_contracts_clicked)
        self._ui.pushButton_bills.clicked.connect(self._controller.on_pushButton_bills_clicked)
        self._ui.pushButton_manufacturers.clicked.connect(self._controller.on_pushButton_manufacturers_clicked)
        self._ui.pushButton_orders.clicked.connect(self._controller.on_pushButton_orders_clicked)

        # Tab 1
        self._ui._1_pushButton_new_order.clicked.connect(self._controller._1_products_tab.on_1_pushButton_new_order_clicked)

        # Tab 5
        self._ui._5_pushButton_new_manufacturer.clicked.connect(self._controller._5_manufacturers_tab.on_pushButton_new_menufacturer_clicked)
        self._ui._5_pushButton_edit.clicked.connect(self._controller._5_manufacturers_tab.on_pushButton_edit_clicked)
        self._ui._5_pushButton_update.clicked.connect(self._controller._5_manufacturers_tab.on_pushButton_update_clicked)
        self._ui._5_pushButton_edit_products.clicked.connect(self._controller._5_manufacturers_tab.on_pushButton_edit_products_clicked)

    @pyqtSlot(int)
    def on_stackedWidget_currentChanged(self, index):
        controllers = [
            self._controller._1_products_tab,
            self._controller._2_warehouses_tab,
            self._controller._3_contracts_tab,
            self._controller._4_bills_tab,
            self._controller._5_manufacturers_tab,
            self._controller._6_orders_tab
        ]
        controllers[index].update()

