from views.gen.ui_main_view import Ui_MainWindow
from PyQt5.QtCore import QObject, pyqtSlot
from controllers.main_controller import MainController

class MainController_2_Warehouses(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui

    def update(var):
        print('Updating 2st controller')
