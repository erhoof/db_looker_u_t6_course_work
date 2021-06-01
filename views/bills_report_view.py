from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.gen.ui_bills_report_view import Ui_bills_report_view

class BillsReportView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_bills_report_view()
        self._controller = controller
        self._controller._ui = self._ui
        self._controller._view = self
        
        self._ui.setupUi(self)

        self._ui.pushButton_create.clicked.connect(self._controller.on_pushButton_create_clicked)