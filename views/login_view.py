from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from views.gen.ui_login_view import Ui_LoginWindow

class LoginView(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._ui = Ui_LoginWindow()
        self._controller = controller
        self._controller._ui = self._ui
        self._controller._view = self
        
        self._ui.setupUi(self)

        self._ui.loginButton.clicked.connect(self._controller.on_login_button_clicked)