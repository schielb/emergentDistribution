from random import randint
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from emergence_ui import Ui_Dialog
from emergence_magic import emerge_step
import sys

colors = ["white", "red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]

# Debug note: Main text box is 30 tall and 60 wide

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.vals = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
        ]

        self.boxes = [
            [self.ui.textEdit_1_1, self.ui.textEdit_1_2, self.ui.textEdit_1_3, self.ui.textEdit_1_4, 
             self.ui.textEdit_1_5, self.ui.textEdit_1_6, self.ui.textEdit_1_7, self.ui.textEdit_1_8, 
             self.ui.textEdit_1_9, self.ui.textEdit_1_10],
            [self.ui.textEdit_2_1, self.ui.textEdit_2_2, self.ui.textEdit_2_3, self.ui.textEdit_2_4, 
             self.ui.textEdit_2_5, self.ui.textEdit_2_6, self.ui.textEdit_2_7, self.ui.textEdit_2_8, 
             self.ui.textEdit_2_9, self.ui.textEdit_2_10],
            [self.ui.textEdit_3_1, self.ui.textEdit_3_2, self.ui.textEdit_3_3, self.ui.textEdit_3_4, 
             self.ui.textEdit_3_5, self.ui.textEdit_3_6, self.ui.textEdit_3_7, self.ui.textEdit_3_8, 
             self.ui.textEdit_3_9, self.ui.textEdit_3_10],
            [self.ui.textEdit_4_1, self.ui.textEdit_4_2, self.ui.textEdit_4_3, self.ui.textEdit_4_4, 
             self.ui.textEdit_4_5, self.ui.textEdit_4_6, self.ui.textEdit_4_7, self.ui.textEdit_4_8, 
             self.ui.textEdit_4_9, self.ui.textEdit_4_10],
            [self.ui.textEdit_5_1, self.ui.textEdit_5_2, self.ui.textEdit_5_3, self.ui.textEdit_5_4, 
             self.ui.textEdit_5_5, self.ui.textEdit_5_6, self.ui.textEdit_5_7, self.ui.textEdit_5_8, 
             self.ui.textEdit_5_9, self.ui.textEdit_5_10],
            [self.ui.textEdit_6_1, self.ui.textEdit_6_2, self.ui.textEdit_6_3, self.ui.textEdit_6_4, 
             self.ui.textEdit_6_5, self.ui.textEdit_6_6, self.ui.textEdit_6_7, self.ui.textEdit_6_8, 
             self.ui.textEdit_6_9, self.ui.textEdit_6_10],
            [self.ui.textEdit_7_1, self.ui.textEdit_7_2, self.ui.textEdit_7_3, self.ui.textEdit_7_4, 
             self.ui.textEdit_7_5, self.ui.textEdit_7_6, self.ui.textEdit_7_7, self.ui.textEdit_7_8, 
             self.ui.textEdit_7_9, self.ui.textEdit_7_10],
            [self.ui.textEdit_8_1, self.ui.textEdit_8_2, self.ui.textEdit_8_3, self.ui.textEdit_8_4, 
             self.ui.textEdit_8_5, self.ui.textEdit_8_6, self.ui.textEdit_8_7, self.ui.textEdit_8_8, 
             self.ui.textEdit_8_9, self.ui.textEdit_8_10],
            [self.ui.textEdit_9_1, self.ui.textEdit_9_2, self.ui.textEdit_9_3, self.ui.textEdit_9_4, 
             self.ui.textEdit_9_5, self.ui.textEdit_9_6, self.ui.textEdit_9_7, self.ui.textEdit_9_8, 
             self.ui.textEdit_9_9, self.ui.textEdit_9_10],
            [self.ui.textEdit_10_1, self.ui.textEdit_10_2, self.ui.textEdit_10_3, self.ui.textEdit_10_4, 
             self.ui.textEdit_10_5, self.ui.textEdit_10_6, self.ui.textEdit_10_7, self.ui.textEdit_10_8, 
             self.ui.textEdit_10_9, self.ui.textEdit_10_10]
        ]

        self.fillBoxes()

        self.ui.random_pushButton.clicked.connect(self.randomizeBoxes)
        self.ui.grid_slider.valueChanged.connect(self.changeGrid)

        self.gridLayout = 0

        #self.messageTimer = QTimer()
        #self.messageTimer.timeout.connect(self.check_ui_updates)


    def fillBoxes(self, random=False):
        
        rows = int(self.ui.rowsNum_comboBox.currentText())
        cols = int(self.ui.colsNum_comboBox.currentText())
        numV = int(self.ui.varNum_comboBox.currentText())

        for r in range(10):
            for c in range(10):
                if r < rows and c < cols:
                    if random:
                        self.vals[r][c] = randint(1, numV)
                        
                    color = colors[self.vals[r][c]]
                    self.boxes[r][c].setStyleSheet("background: " + color)
                else:
                    self.boxes[r][c].setStyleSheet("background: black")

    def randomizeBoxes(self):
        self.fillBoxes(random=True)

    # TODO: finish this
    def changeGrid(self):
        if self.gridLayout == self.ui.grid_slider.value():
            return
        else:
            print("Not implemented yet")
            self.ui.grid_slider.setValue(0)

    def step(self):
        rows = int(self.ui.rowsNum_comboBox.currentText())
        cols = int(self.ui.colsNum_comboBox.currentText())
        numV = int(self.ui.varNum_comboBox.currentText())
        
        tmp = emerge_step(self.vals, rows, cols, numV)
        self.vals = tmp
        self.fillBoxes()





def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    
    ret = app.exec_()
    #application.check_signOut()
    sys.exit(ret)
    


if __name__ == "__main__":
    main()