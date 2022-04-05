import copy
from random import randint
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from emergence_ui import Ui_Dialog
from emergence_magic import emerge_step
from emergence_history import History
import sys
import random
import time

ADVANCE_INTERVAL_MS = 500
INIT_WHITE = 8
INIT_BLACK = 9


colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta", "white", "black"]


# This is the main class of the application where all functions relative to the buttons go
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.history = History()

        # Make the random seed predicatble or truly random
        #random.seed(time.time())
        random.seed(0xBEEFCAFE)

        self.vals = [
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
            [INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE,INIT_WHITE],
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

        self.ui.colsNum_comboBox.currentIndexChanged.connect(self.randomizeBoxes)
        self.ui.rowsNum_comboBox.currentIndexChanged.connect(self.randomizeBoxes)
        self.ui.varNum_comboBox.currentIndexChanged.connect(self.randomizeBoxes)
        self.ui.random_pushButton.clicked.connect(self.randomizeBoxes)
        self.ui.grid_slider.valueChanged.connect(self.changeGrid)

        self.gridLayout = 0

        self.advanceTimer = QTimer()
        self.advanceTimer.setInterval(ADVANCE_INTERVAL_MS)
        self.advanceTimer.timeout.connect(self.autoStep)

        self.ui.step_pushButton.clicked.connect(self.step_step)
        self.ui.checkBox.clicked.connect(self.toggleAutoStep)
        self.ui.next_pushButton.clicked.connect(self.step_forward)
        self.ui.prev_pushButton.clicked.connect(self.step_backward)
        self.ui.return_pushButton.clicked.connect(self.step_return)

        self.randomizeBoxes()


    ### GRID FUNCTIONS
    ###############################################################
    ### Fill stuff
    def fillBoxes(self, random=False):
        
        rows = int(self.ui.rowsNum_comboBox.currentText())
        cols = int(self.ui.colsNum_comboBox.currentText())
        numV = int(self.ui.varNum_comboBox.currentText())

        for r in range(10):
            for c in range(10):
                if r < rows and c < cols:
                    if random:
                        self.vals[r][c] = randint(0, numV-1)
                        
                    color = colors[self.vals[r][c]]
                else:
                    color = colors[INIT_BLACK]
                self.boxes[r][c].setStyleSheet("background: " + color)

        if random:
            self.history.clear()
            self.history.push(self.vals)

    def randomizeBoxes(self):
        self.fillBoxes(random=True)

    # TODO: finish this
    ### Grid stuff
    def changeGrid(self):
        if self.gridLayout == self.ui.grid_slider.value():
            return
        else:
            print("Not implemented yet")
            self.ui.grid_slider.setValue(0)
    ###############################################################

    ### MAGIC ###
    ###############################################################
    def step_emerge(self):
        rows = int(self.ui.rowsNum_comboBox.currentText())
        cols = int(self.ui.colsNum_comboBox.currentText())
        numV = int(self.ui.varNum_comboBox.currentText())
        
        tmp = emerge_step(self.vals, rows, cols, numV)
        self.vals = copy.deepcopy(tmp)
        self.history.push(self.vals)
        self.fillBoxes()
    ###############################################################

    ### STEP FUNCTIONS ###
    ###############################################################
    # In all of these I either generate new data or review old data;
    #  this then gets displayed, and I update the buttons accordingly
    ### Manual steps
    def step_step(self):
        self.step_emerge()
        canMove = self.history.canStillMove()
        self.ui.prev_pushButton.setEnabled(canMove[0])
        self.ui.next_pushButton.setEnabled(canMove[1])
        self.ui.step_pushButton.setEnabled(not canMove[1])
        self.ui.return_pushButton.setEnabled(False)
    
    def step_forward(self):
        self.vals = copy.deepcopy(self.history.getNext())
        self.fillBoxes()

        canMove = self.history.canStillMove()
        self.ui.prev_pushButton.setEnabled(canMove[0])
        self.ui.next_pushButton.setEnabled(canMove[1])
        self.ui.step_pushButton.setEnabled(not canMove[1])
        self.ui.return_pushButton.setEnabled(canMove[1])

    def step_backward(self):
        self.vals = copy.deepcopy(self.history.getPrev())
        self.fillBoxes()

        canMove = self.history.canStillMove()
        self.ui.prev_pushButton.setEnabled(canMove[0])
        self.ui.next_pushButton.setEnabled(canMove[1])
        self.ui.step_pushButton.setEnabled(False)
        self.ui.return_pushButton.setEnabled(canMove[1])

    def step_return(self):
        self.vals = copy.deepcopy(self.history.getReturn())
        self.fillBoxes()
        self.ui.next_pushButton.setEnabled(False)
        self.ui.prev_pushButton.setEnabled(False)
        self.ui.step_pushButton.setEnabled(True)
        self.ui.return_pushButton.setEnabled(False)
        

    ### Auto step
    def autoStep(self):
        self.step_emerge()

    def toggleAutoStep(self):
        if self.ui.checkBox.isChecked():
            self.advanceTimer.start()
            self.ui.next_pushButton.setEnabled(False)
            self.ui.prev_pushButton.setEnabled(False)
            self.ui.step_pushButton.setEnabled(False)
        else:
            self.advanceTimer.stop()
            self.ui.prev_pushButton.setEnabled(True)
            self.ui.next_pushButton.setEnabled(False)
            self.ui.step_pushButton.setEnabled(True)
    ###############################################################





def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    
    ret = app.exec_()
    #application.check_signOut()
    sys.exit(ret)
    


if __name__ == "__main__":
    main()