from controllers.add_m_products_controller import AddMProductsController
from PyQt5.QtWidgets import QMessageBox
from views.new_manufacturer_view import NewManufacturerView
from views.add_m_products_view import AddMProductsView
from PyQt5.QtCore import QAbstractItemModel, QItemSelection, QModelIndex, pyqtSlot
from controllers.main_controller import MainController
from model.manager_core import ManagerCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from controllers.new_manufacturer_controller import NewManufacturerController
from model.MEditProducts_model import EditMProductsTableModel

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
        self._id = 0

        for id, name in ManagerCore().cursor:
            item = QStandardItem(f'({id}) {name}')
            self._list_model.appendRow(item)

        # Count of manufacturers
        ManagerCore().cursor.execute('''
            SELECT COUNT(id) FROM manufacturers
        ''')
        self._ui._5_label_manufacturers_count.setText(f'Кол-во: {ManagerCore().cursor.fetchall()[0][0]}')

    
    def update_products_table(self):
        if not self._id: return

        # Prepare table
        print('NEWID:',self._id)
        data = ManagerCore().cursor.execute('''
            SELECT * FROM products WHERE manufacturer_id=?
        ''', str(self._id)).fetchall()
        self._table_model = EditMProductsTableModel(data)
        self._ui._5_tableView_products.setModel(self._table_model)


    @pyqtSlot(QModelIndex, QModelIndex)
    def on_listView_manufacturers_rowSelected(self, selected: QModelIndex):
        string = str(self._list_model.data(selected))
        self._id = string[string.find('(')+1: string.find(')')]

        # Get data
        ManagerCore().cursor.execute(f'''
            SELECT id, name, address, ceo_fullname, accountant_fullname, requisites 
                FROM manufacturers
                WHERE id={selected.row()+1}
        ''')
        res = ManagerCore().cursor.fetchall()[0]
        
        # Fill up with data
        self._ui._5_label_manufacturer_id.setText(str(res[0]))
        self._ui._5_lineEdit_manufacturer_name.setText(res[1])
        self._ui._5_lineEdit_address.setText(res[2])
        self._ui._5_lineEdit_CEO.setText(res[3])
        self._ui._5_lineEdit_accountant.setText(res[4])
        self._ui._5_lineEdit_requisites.setText(res[5])
        self.update_products_table()

        # Activate buttons
        self._ui._5_pushButton_edit_products.setEnabled(True)
        self._ui._5_pushButton_edit.setEnabled(True)
        self._ui._5_pushButton_update.setEnabled(True)


    @pyqtSlot()
    def on_pushButton_new_menufacturer_clicked(self):
        self._new_dialog_controller = NewManufacturerController(self, None)
        self._new_dialog_view = NewManufacturerView(self._new_dialog_controller)
        self._new_dialog_view.show()

    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        if self._id == 0: return

        name = self._ui._5_lineEdit_manufacturer_name.text()
        address = self._ui._5_lineEdit_address.text()
        CEO = self._ui._5_lineEdit_CEO.text()
        accountant = self._ui._5_lineEdit_accountant.text()
        requisites = self._ui._5_lineEdit_requisites.text()

        if not name or not address or not CEO or not requisites:
            QMessageBox.warning('Ошибка ввода', 'Не заполнены необходимые поля')
            return

        print(self._id)
        ManagerCore().cursor.execute('''
            UPDATE manufacturers
                SET name = ?,
                    address = ?,
                    ceo_fullname = ?,
                    accountant_fullname = ?,
                    requisites = ?
                WHERE id = ?''', (name, address, CEO, accountant, requisites, self._id))
        ManagerCore().db_connect.commit()
        #self._ui._5_listView_manufacturers.setCurrentIndex(self._list_model.createIndex(int(self._id)-1, 0))

    @pyqtSlot()
    def on_pushButton_update_clicked(self):
        self.update_products_table()

    @pyqtSlot()
    def on_pushButton_edit_products_clicked(self):
        self._new_edit_dialog_controller = AddMProductsController(self._id)
        self._new_edit_dialog_view = AddMProductsView(self._new_edit_dialog_controller)
        self._new_edit_dialog_view.show()
