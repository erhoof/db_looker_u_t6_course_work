from model.manager_core import ManagerCore
from controllers.login_controller import LoginController
import sys
from PyQt5.QtWidgets import QApplication

from views.login_view import LoginView
import logging

class App(QApplication):
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.login_controller = LoginController()
        self.login_view = LoginView(self.login_controller)
        self.login_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    app.setStyle('Fusion')
    sys.exit(app.exec_()) 
