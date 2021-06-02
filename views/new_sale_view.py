from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.gen.ui_new_sale_view import Ui_new_sale_view

class NewSaleView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_new_sale_view()
        self._controller = controller
        self._controller._ui = self._ui
        self._controller._view = self
        
        self._ui.setupUi(self)

        self._ui.spinBox.valueChanged.connect(self._controller.on_spinBox_currentValue_changed)
        self._ui.pushButton.clicked.connect(self._controller.on_pushButton_clicked)