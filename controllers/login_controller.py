from views.main_view import MainView
from controllers.main_controller import MainController
from views.gen.ui_login_view import Ui_LoginWindow
from model.manager_core import ManagerCore
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
import logging

class LoginController(QObject):

    def __init__(self, ui: Ui_LoginWindow = None):
        super().__init__()
        self._ui = ui

    @pyqtSlot()
    def on_login_button_clicked(self):
        login = self._ui.loginEdit.text()
        password = self._ui.passwordEdit.text()
        db_filename = self._ui.lineEdit_file.text()

        #if not login:
        #    login = 'admin'
        #if not password:
        #    password = 'admin'
        if not db_filename:
            db_filename = 'core.db'

        print(login, password, db_filename)

        # db with this filename was not found
        session = ManagerCore().create_session(login, password, db_filename) 
        if session == 1:
            msg = QMessageBox.question(None,
             'Файл не найден',
              f'Создать БД с именем \'{db_filename}\'?',
              QMessageBox.Yes | QMessageBox.No, QMessageBox. Yes)
            if msg == QMessageBox.Yes:
                ManagerCore().create_db_file(db_filename)
                login = 'admin'
                password = 'admin'
                QMessageBox.about(None, 'Создание файла', 'Файл успешно создан\nДанные для входа: admin/admin')
            else:
                logging.info('DB Create: deny')
                return
        elif session == 2:
            QMessageBox.warning(None, 'Ошибка', 'Неверно введен логин/пароль')
            return

        self._main_controller = MainController(None)
        self._main_view = MainView(self._main_controller)
        self._main_view.show()
        self._view.close()

        


        
            

        
