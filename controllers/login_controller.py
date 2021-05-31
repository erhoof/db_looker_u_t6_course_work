from views.gen.ui_login_view import Ui_LoginWindow
from model.manager_core import ManagerCore
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
import logging

class LoginController(QObject):

    def __init__(self):
        super().__init__()
        self._ui = Ui_LoginWindow()

    @pyqtSlot()
    def on_login_button_clicked(self):
        login = self._ui.loginEdit.text()
        password = self._ui.passwordEdit.text()
        db_filename = self._ui.lineEdit_file.text()

        if not login:
            login = 'admin'
        if not password:
            password = 'admin'
        if not db_filename:
            db_filename = 'core.db'

        print(login, password, db_filename)

        # db with this filename was not found
        if ManagerCore().create_session(login, password, db_filename) == 1:
            msg = QMessageBox.question(None,
             'Файл не найден',
              f'Создать БД с именем \'{db_filename}\'?',
              QMessageBox.Yes | QMessageBox.No, QMessageBox. Yes)
            if msg == QMessageBox.Yes:
                ManagerCore().create_db_file(db_filename)
                logging.info('DB Create: accept')
            else:
                logging.info('DB Create: deny')
            

        
