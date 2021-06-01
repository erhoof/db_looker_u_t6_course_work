from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.gen.ui_new_order_view import Ui_NewOrderView

class NewOrderView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_NewOrderView()
        self._ui.setupUi(self)

        self._controller = controller
        self._controller._ui = self._ui
        self._controller._view = self
        self._controller.update()

        self._ui.listView_manufacturers.selectionModel().currentChanged.connect(self._controller.on_listView_manufactures_rowSelected)
        self._ui.pushButton_add_manufacturer.clicked.connect(self._controller.on_pushButton_add_manufacturer_clicked)
        self._ui.pushButton_add_product.clicked.connect(self._controller.on_pushButton_add_product_clicked)
        self._ui.spinBox_count.valueChanged.connect(self._controller.on_spinbox_count_valueChanged)
        self._ui.pushButton_remove.clicked.connect(self._controller.on_pushButton_remove_clicked)
        self._ui.pushButton_cancel.clicked.connect(self._controller.on_pushButton_cancel_clicked)
        self._ui.pushButton_make_a_deal.clicked.connect(self._controller.on_pushButton_make_a_deal_clicked)
