import sys
from PyQt5.QtWidgets import QApplication
from views.login_view import LoginView

class App(QApplication):
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.login_view = LoginView()
        self.login_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_()) 
