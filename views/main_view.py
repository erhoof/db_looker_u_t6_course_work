from PyQt5.QtWidgets import QMainWindow

from views.gen.ui_main_view import Ui_MainWindow

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)