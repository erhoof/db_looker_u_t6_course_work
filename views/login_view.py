from PyQt5.QtWidgets import QMainWindow

from views.gen.ui_login_view import Ui_LoginWindow

class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_LoginWindow()
        self._ui.setupUi(self)