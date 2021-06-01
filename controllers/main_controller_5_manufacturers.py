from views.new_manufacturer_view import NewManufacturerView
from PyQt5.QtCore import QItemSelection, QModelIndex, pyqtSlot
from controllers.main_controller import MainController
from model.manager_core import ManagerCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from controllers.new_manufacturer_controller import NewManufacturerController

class MainController_5_Manufacturers(MainController):

    def __init__(self, parent: MainController):
        super().__init__()
        self._parent = parent
        self._ui = parent._ui

        # Setup models
        self._list_model = QStandardItemModel()
        self._ui._5_listView_manufacturers.setModel(self._list_model)

        # Connect slots/signals
        self._ui._5_listView_manufacturers.selectionModel().currentChanged.connect(self.on_listView_manufacturers_rowSelected)
        
    def update(self):
        # Get manufacturers
        ManagerCore().cursor.execute('''
            SELECT id, name FROM manufacturers
        ''')
        
        # Fill Up list of manufacturers
        self._list_model.clear()

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_model.appendRow(item)

    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_manufacturers_rowSelected(self, selected: QModelIndex):
        print(selected.row())

    @pyqtSlot()
    def on_pushButton_new_menufacturer_clicked(self):
        self._new_dialog_controller = NewManufacturerController(self, None)
        self._new_dialog_view = NewManufacturerView(self._new_dialog_controller)
        self._new_dialog_view.show()
