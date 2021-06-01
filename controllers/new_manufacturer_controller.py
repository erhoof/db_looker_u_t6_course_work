from model.manager_core import ManagerCore
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QMessageBox
from views.gen.ui_new_manufacturer import Ui_NewManufacturer
from model.manager_core import ManagerCore

class NewManufacturerController(QObject):

    def __init__(self, parent, ui: Ui_NewManufacturer = None):
        super().__init__()
        self._ui = ui
        self._parent = parent

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        if not self._ui.lineEdit_name or \
            not self._ui.lineEdit_requisites or \
            not self._ui.lineEdit_address or \
            not self._ui.lineEdit_CEO:
            QMessageBox.warning('Ошибка ввода', 'Не все необходимые поля заполнены')
            return

        #TODO: check if it's nessesary
        if not self._ui.lineEdit_accountant.text():
            self._ui.lineEdit_accountant = ''
        
        ManagerCore().cursor.execute('''
            INSERT INTO manufacturers 
                (name, address, ceo_fullname, accountant_fullname, requisites)
                VALUES (?, ?, ?, ?, ?)
        ''', (self._ui.lineEdit_name.text(),
                self._ui.lineEdit_address.text(),
                self._ui.lineEdit_CEO.text(),
                self._ui.lineEdit_accountant.text(),
                self._ui.lineEdit_requisites.text()))
        ManagerCore().db_connect.commit()
        self._parent.update()
        self._view.close()

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self._view.close()