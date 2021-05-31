from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot
from controllers.main_controller import MainController

class MainController_2_Warehouses(MainController):

    def __init__(self, ui: Ui_MainWindow = None):
        super().__init__()
        self._ui = ui