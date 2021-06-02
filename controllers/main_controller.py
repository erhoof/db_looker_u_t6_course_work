from model.manager_core import ManagerCore
from PyQt5.QtWidgets import QInputDialog
import bcrypt
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot

class MainController(QObject):

    def __init__(self, ui: Ui_MainWindow = None):
        super().__init__()
        self._ui = ui
        self._1_products_tab = None
        self._2_warehouses_tab = None
        self._3_contracts_tab = None
        self._4_bills_tab = None
        self._5_manufacturers_tab = None
        self._6_orders_tab = None

    def update(var):
        pass

    def enable_all_tab_buttons(self):
        self._ui.pushButton_products.setEnabled(True)
        self._ui.pushButton_warehouses.setEnabled(True)
        self._ui.pushButton_contracts.setEnabled(True)
        self._ui.pushButton_bills.setEnabled(True)
        self._ui.pushButton_manufacturers.setEnabled(True)
        self._ui.pushButton_orders.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_products_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(0)
        self.enable_all_tab_buttons()
        self._ui.pushButton_products.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_warehouses_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(1)
        self.enable_all_tab_buttons()
        self._ui.pushButton_warehouses.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_contracts_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(2)
        self.enable_all_tab_buttons()
        self._ui.pushButton_contracts.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_bills_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(3)
        self.enable_all_tab_buttons()
        self._ui.pushButton_bills.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_manufacturers_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(4)
        self.enable_all_tab_buttons()
        self._ui.pushButton_manufacturers.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_orders_clicked(self):
        self._ui.stackedWidget.setCurrentIndex(5)
        self.enable_all_tab_buttons()
        self._ui.pushButton_orders.setEnabled(False)

    @pyqtSlot(bool)
    def on_action_users_clicked(self):
        password = QInputDialog.getText(None, 'Смена пароля', 'Введите пароль для пользователя admin:')
        password_hash = bcrypt.hashpw(password[0].encode(), bcrypt.gensalt(12))

        ManagerCore().cursor.execute(f'''
            UPDATE users
                SET password_hash = ?
                    WHERE login = ?''',
                (password_hash, 'admin'))
        ManagerCore().db_connect.commit()



        
    
