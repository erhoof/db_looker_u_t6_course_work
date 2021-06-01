from controllers.new_manufacturer_controller import NewManufacturerController
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.gen.ui_new_manufacturer import Ui_NewManufacturer

class NewManufacturerView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_NewManufacturer()
        self._controller: NewManufacturerController = controller
        self._controller._ui = self._ui
        self._controller._view = self
        
        self._ui.setupUi(self)

        self._ui.buttonBox.accepted.connect(self._controller.on_buttonBox_accepted)
        self._ui.buttonBox.rejected.connect(self._controller.on_buttonBox_accepted)