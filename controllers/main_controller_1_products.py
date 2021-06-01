from model.manager_core import ManagerCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel
from controllers.main_controller import MainController
from model.manager_core import ManagerCore
import sqlite3

class MainController_1_Products(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui
        
    def update(self):
        pass

    @pyqtSlot()
    def on_1_pushButton_new_order_clicked(self):
        print('Got it!')
