from controllers.add_m_products_controller import AddMProductsController
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QAbstractTableModel, pyqtSlot
from views.gen.ui_m_add_products_view import Ui_m_add_products_view

class AddMProductsView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_m_add_products_view()
        self._ui.setupUi(self)

        self._controller: AddMProductsController = controller
        self._controller._ui = self._ui
        self._controller._view = self
        self._controller.update()

        self._ui.pushButton_add.clicked.connect(self._controller.on_pushButton_add_clicked)
        self._ui.tableView_products.selectionModel().selectionChanged.connect(self._controller.on_table_cell_clicked)
        self._ui.pushButton_edit.clicked.connect(self._controller.on_pushButton_edit_clicked)
        self._ui.pushButton_remove.clicked.connect(self._controller.on_pushButton_remove_clicked)
