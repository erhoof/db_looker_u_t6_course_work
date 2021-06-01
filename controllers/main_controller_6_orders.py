from controllers.main_controller import MainController
from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot
from controllers.main_controller import MainController
from controllers.new_order_controller import NewOrderController
from views.new_order_view import NewOrderView

class MainController_6_Orders(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui


