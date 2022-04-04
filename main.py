import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from emergence_ui import Ui_Dialog
import sys

exited = False

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)




def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    
    ret = app.exec_()
    #application.check_signOut()
    sys.exit(ret)
    


if __name__ == "__main__":
    main()