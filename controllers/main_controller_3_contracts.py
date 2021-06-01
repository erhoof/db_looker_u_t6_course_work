from views.new_order_view import NewOrderView
from controllers.new_order_controller import NewOrderController
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot
from controllers.main_controller import MainController

class MainController_3_Contracts(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui


    @pyqtSlot()
    def on_pushButton_newContract_clicked(self):
        self._new_order_controller = NewOrderController()
        self._new_order_view = NewOrderView(self._new_order_controller)
        self._new_order_view.show()