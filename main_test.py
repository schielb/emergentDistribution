import copy
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer
from emergence_ui_test import Ui_Dialog
from emergence_magic import emerge_step, getSurrounding
from assign_loop_magic import assign_loop_step
from rand_loop_magic import rand_loop_step
from random_magic import random_step
from emergence_history import History
from functools import partial
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from random import randint
import sys

colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta", "black"]
INIT_BLACK = 8

EMERGENCE_INDEX = 3
ASSIGN_LOOP_INDEX = 2
RAND_LOOP_INDEX = 1
RANDOM_INDEX = 0
solution_steps = {
    RANDOM_INDEX: random_step, RAND_LOOP_INDEX: rand_loop_step,
    ASSIGN_LOOP_INDEX: assign_loop_step, EMERGENCE_INDEX: emerge_step
}

BUTTON_INDEX = ROW_INDEX = HIST_INDEX = 0
COLOR_INDEX  = COL_INDEX = LABL_INDEX = 1

ADVANCE_INTERVAL_MS = 1000


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

        self.numV = 2

        self.ui.rows_spinBox.valueChanged.connect(self.create_new_map)
        self.ui.cols_spinBox.valueChanged.connect(self.create_new_map)
        self.ui.varNum_comboBox.currentIndexChanged.connect(self.change_num_vars)
        self.ui.solution_comboBox.currentIndexChanged.connect(self.change_solution)
        self.ui.randomOnOff_pushButton.clicked.connect(self.toggle_on_off)
        self.ui.percentOff_spinBox.valueChanged.connect(self.randomize_on_off)

        self.onOff = True

        self.boxes : dict = {}
        self.vals = []
        '''
        The self.boxes dictionary is formatted like so:
            key     -> tuple(row, column)
            value   -> list(button, color index)
        
        The self.vals list is a 2d array that contains the color indices
        '''
        self.histogram_total = {
            0: (self.ui.var1_progressBar, self.ui.varBar1_label),
            1: (self.ui.var2_progressBar, self.ui.varBar2_label),
            2: (self.ui.var3_progressBar, self.ui.varBar3_label),
            3: (self.ui.var4_progressBar, self.ui.varBar4_label),
            4: (self.ui.var5_progressBar, self.ui.varBar5_label),
            5: (self.ui.var6_progressBar, self.ui.varBar6_label),
            6: (self.ui.var7_progressBar, self.ui.varBar7_label),
            7: (self.ui.var8_progressBar, self.ui.varBar8_label)
        }
        

        self.histogram_collisions = {
            0: (self.ui.collisions1_progressBar, self.ui.collisionsBar1_label),
            1: (self.ui.collisions2_progressBar, self.ui.collisionsBar2_label),
            2: (self.ui.collisions3_progressBar, self.ui.collisionsBar3_label),
            3: (self.ui.collisions4_progressBar, self.ui.collisionsBar4_label),
            4: (self.ui.collisions5_progressBar, self.ui.collisionsBar5_label),
            5: (self.ui.collisions6_progressBar, self.ui.collisionsBar6_label),
            6: (self.ui.collisions7_progressBar, self.ui.collisionsBar7_label),
            7: (self.ui.collisions8_progressBar, self.ui.collisionsBar8_label)
        }
        self.init_histograms()
        self.analysis_tools_update()

        self.ui.randomVars_pushButton.clicked.connect(self.randomize_vars)
        self.ui.grid_slider.valueChanged.connect(self.changeGrid)

        self.advanceTimer = QTimer()
        self.advanceTimer.setInterval(ADVANCE_INTERVAL_MS)
        self.advanceTimer.timeout.connect(self.autoStep)

        self.ui.step_pushButton.clicked.connect(self.step_step)
        self.ui.checkBox.clicked.connect(self.toggleAutoStep)
        self.ui.next_pushButton.clicked.connect(self.step_forward)
        self.ui.prev_pushButton.clicked.connect(self.step_backward)
        self.ui.return_pushButton.clicked.connect(self.step_return)


        self.fillBoxes(random_vars=True, new_map=True)


    def clear_map(self):
        for key in self.boxes:
            self.boxes[key][BUTTON_INDEX].deleteLater()
        self.boxes.clear()
        
    ### Fill stuff
    def fillBoxes(self, random_vars=False, new_map=False, new_vals=False):
        
        rows = int(self.ui.rows_spinBox.value())
        cols = int(self.ui.cols_spinBox.value())

        if new_map:
            fWidth, fHeight = 1000, 600 #self.ui.map_frame.geometry().height(), self.ui.map_frame.geometry().width()
            bWidth, bHeight = int(fWidth / cols), int(fHeight / rows)

            self.clear_map()
            self.vals.clear()
            bX, bY = 10, 10
            for r in range(rows):
                self.vals.append([])
                for c in range(cols):
                    # Create a new button and place it in the frame
                    button = QtWidgets.QPushButton(self.ui.map_frame)
                    button.setGeometry(QtCore.QRect(bX, bY, bWidth - 2, bHeight - 2))
                    name = "button_%d_%d" % (r, c)
                    button.setObjectName(name)

                    # Create its dictionary values for self.boxes;
                    #  Should be [row, col]: [button, color]
                    key_tuple = (r,c)
                    color_int = randint(0, self.numV-1)
                    color = colors[color_int]
                    self.vals[r].append(color_int)
                    button_tuple = [button, color]
                    
                    # Add new key and value to dict; add button click action
                    self.boxes[key_tuple] = button_tuple 
                    button.clicked.connect(partial(self.click_q, key_tuple)) 

                    bX += bWidth
                bY += bHeight  
                bX = 10    

        if random_vars:
            for key in self.boxes:
                color_int = randint(0, self.numV-1)
                self.boxes[key][COLOR_INDEX] = color_int
                self.vals[key[ROW_INDEX]][key[COL_INDEX]] = color_int

        if new_vals:
            for i in range(len(self.vals)):
                for j in range(len(self.vals[i])):
                    key = (i, j)
                    self.boxes[key][COLOR_INDEX] = self.vals[i][j]

        for key in self.boxes:
            color_int = self.boxes[key][1]
            color = colors[color_int]
            self.boxes[key][BUTTON_INDEX].setStyleSheet("background: " + color)  

        self.run_alaysis()                 

        if random_vars or new_map:
            self.history.clear()
            self.history.push(self.vals)
            self.step_updateButtons()

    ### Grid stuff - square or hexagonal
    def changeGrid(self):
        # Start by getting the general geometry of the boxes
        # TODO THESE ARE MAGIC NUMBERS! FIX WHEN YOU CAN CHANGE MAP DIMENSIONS!
        leftEdge = 10
        separation = 10

        if not self.ui.grid_slider.value():
            # Here we want to transition to hexagonal
            init_pos = int(leftEdge + (separation / 2))
        else:
            # This would be square grid
            init_pos = int(leftEdge)
            
        # Shift each other row right/left by ~five pixels
        rows = int(self.ui.rows_spinBox.value())
        cols = int(self.ui.cols_spinBox.value())
        for i in range(1,rows,2):
            pos = init_pos
            for j in range(cols):
                key = (i, j)
                cur = self.boxes[key][BUTTON_INDEX].geometry().getRect()
                self.boxes[key][BUTTON_INDEX].setGeometry(pos, cur[1], cur[2], cur[3])
                pos += separation


        '''for i in range(1,rows,2):
            pos = init_pos
            for j in range(10):
                cur = self.boxes[i][j].geometry().getRect()
                self.boxes[i][j].setGeometry(pos, cur[1], cur[2], cur[3])
                pos += separation'''

        self.randomize_vars()

    

    def randomize_vars(self):
        if self.ui.solution_comboBox.currentIndex() == ASSIGN_LOOP_INDEX:
            
            color_int = 0
            for key in self.boxes:
                if self.boxes[key][COLOR_INDEX] != INIT_BLACK:
                    color = colors[color_int]
                    self.boxes[key][BUTTON_INDEX].setStyleSheet("background: " + color)
                    self.boxes[key][COLOR_INDEX] = color_int
                    self.vals[key[ROW_INDEX]][key[COL_INDEX]] = color_int

                    color_int = (color_int + 1) % self.numV

        else:
            self.fillBoxes(random_vars=True) 

    def seed_clusters(self, final_goal_percent=50, num_rounds=10, empty=True):
        # We want to ensure first off that we have a fully filled map
        self.create_new_map()

        new_vals = copy.deepcopy(self.vals)

        # Start py putting the seed in
        initial_percent = float(float(final_goal_percent / 10) / 100)



    def create_new_map(self):
        self.fillBoxes(new_map=True)

    def toggle_on_off(self):
        if self.onOff:
            self.ui.randomOnOff_pushButton.setText('Turn All On')
            self.ui.percentOff_spinBox.setEnabled(True)
        else:
            self.ui.randomOnOff_pushButton.setText('Randomize On/Off') 
            self.ui.percentOff_spinBox.setEnabled(False)

        self.onOff = not self.onOff
        self.randomize_on_off()
        
    def change_num_vars(self):
        self.numV = int(self.ui.varNum_comboBox.currentText())
        self.randomize_vars()
        self.analysis_tools_update()

    def randomize_on_off(self):
        if not self.onOff:
            
            for key in self.boxes:
                # Chance is proportional to number of vars
                color_int = INIT_BLACK \
                    if randint(0, 10) <= (self.ui.percentOff_spinBox.value() / 10)  \
                    else randint(0, self.numV-1)

                color = colors[color_int]
                self.boxes[key][BUTTON_INDEX].setStyleSheet("background: " + color)
                self.boxes[key][COLOR_INDEX] = color_int
                self.vals[key[ROW_INDEX]][key[COL_INDEX]] = color_int
            # Call this in case we need to keep some sort of order; lost work earlier, but we'll survive
            if self.ui.solution_comboBox.currentIndex() == ASSIGN_LOOP_INDEX:
                self.randomize_vars()
                return
                
        else:
            for key in self.boxes:
                color_int = 0
                color = colors[color_int]
                self.boxes[key][BUTTON_INDEX].setStyleSheet("background: " + color)
                self.boxes[key][COLOR_INDEX] = color_int
                self.vals[key[ROW_INDEX]][key[COL_INDEX]] = color_int
            self.randomize_vars()
            return
            
        self.fillBoxes()

    def change_solution(self):
        if self.ui.solution_comboBox.currentIndex() == ASSIGN_LOOP_INDEX:
            self.ui.randomVars_pushButton.setText('Initialize Vars')
        else:
            self.ui.randomVars_pushButton.setText('Randomize Vars')
        
        if not self.onOff:
            self.toggle_on_off() # Runs the process of creating the map already
        else:
            self.randomize_vars()
            
    
    def click_q(self, num):
        color_int = self.boxes[num][COLOR_INDEX]

        color_int = randint(0, self.numV-1) \
            if (color_int == INIT_BLACK) \
            else INIT_BLACK

        color = colors[color_int]

        self.boxes[num][BUTTON_INDEX].setStyleSheet("background: " + color)
        self.boxes[num][COLOR_INDEX] = color_int
        self.vals[num[ROW_INDEX]][num[COL_INDEX]] = color_int

        
    ### MAGIC ###
    ###############################################################
    def step_generate(self):
        rows = int(self.ui.rows_spinBox.value())
        cols = int(self.ui.cols_spinBox.value())
        grid = int(self.ui.grid_slider.value())

        step_index = self.ui.solution_comboBox.currentIndex()
        step = solution_steps[step_index]
        
        tmp = step(self.vals, rows, cols, self.numV, grid)
        self.vals = copy.deepcopy(tmp)
        self.history.push(self.vals)
        self.fillBoxes(new_vals=True)

    ###############################################################

    ### STEP FUNCTIONS ###
    ###############################################################
    # In all of these I either generate new data or review old data;
    #  this then gets displayed, and I update the buttons accordingly
    ### Manual steps
    def step_updateButtons(self):
        canMove = self.history.canStillMove()
        self.ui.prev_pushButton.setEnabled(canMove[0])
        self.ui.next_pushButton.setEnabled(canMove[1])
        self.ui.step_pushButton.setEnabled(not canMove[1])
        self.ui.return_pushButton.setEnabled(canMove[1])

    def step_step(self):
        self.step_generate()
        self.step_updateButtons()

    def step_alt(self, fn):
        self.vals = copy.deepcopy(fn())
        self.fillBoxes(new_vals=True)
        self.step_updateButtons()

    def step_forward(self):
        self.step_alt(self.history.getNext)

    def step_backward(self):
        self.step_alt(self.history.getPrev)

    def step_return(self):
        self.step_alt(self.history.getReturn)
        

    ### Auto step
    def autoStep(self):
        self.step_generate()

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

    ### ANALYSIS FUNCTIONS ###
    ###############################################################
    # In all of these I am manipulating the widgets and math used for
    #  analyzing how well-distributed everything is

    def run_alaysis(self):
        self.analyze_totals_histogram()
        self.analyze_collisions_histogram()

    def analysis_tools_update(self):
        # Start with totals histogram
        for i in range(8):
            self.histogram_total[i][HIST_INDEX].setEnabled(i < self.numV)
            self.histogram_collisions[i][HIST_INDEX].setEnabled(i < self.numV)
            if i >= self.numV:
                self.histogram_total[i][HIST_INDEX].setValue(0)
                self.histogram_total[i][LABL_INDEX].setText('--%')

                self.histogram_collisions[i][HIST_INDEX].setValue(0)
                self.histogram_collisions[i][LABL_INDEX].setText('--%')

        total_line_goal = int(103 - (100 / self.numV))
        self.ui.totalGoal_line.setGeometry(20, total_line_goal, 431, 16)
        self.ui.totalGoal_label.setText("Goal: " + str(int(100 / self.numV)) + "%")

    def init_histograms(self):
        for i in range(8):
            color = colors[i]
            self.histogram_total[i][HIST_INDEX].setStyleSheet(
                "QProgressBar::chunk {background-color: " + color + ";}"
            )
            self.histogram_collisions[i][HIST_INDEX].setStyleSheet(          
                "QProgressBar::chunk {background-color: " + color + ";}"            
            )


    ## Totals histogram - update function
    def analyze_totals_histogram(self):
        each, total = self.analyze_totals()
        for i in range(0, self.numV):
            self.histogram_total[i][HIST_INDEX].setValue(int(each[i] / total * 100))
            self.histogram_total[i][LABL_INDEX].setText(str(int(each[i] / total * 100)) + "%")

    def analyze_collisions_histogram(self):
        each, total = self.analyze_collisions()
        for i in range(0, self.numV):
            self.histogram_collisions[i][HIST_INDEX].setValue(int(each[i] / total[i] * 100))
            self.histogram_collisions[i][LABL_INDEX].setText(str(int(each[i] / total[i] * 100)) + "%")

    def analyze_collisions(self):
        rows = int(self.ui.rows_spinBox.value())
        cols = int(self.ui.cols_spinBox.value())
        grid = int(self.ui.grid_slider.value())

        each = [0 for i in range(8)]
        total = [0 for i in range(8)]
        
        for key in self.boxes:
            # Skip a sqaure if it's black
            if self.boxes[key][COLOR_INDEX] == INIT_BLACK:
                continue

            r, c = key[ROW_INDEX], key[COL_INDEX]
            surrounding = getSurrounding(r, c, rows, cols, grid)

            del surrounding[0]

            # We now have a list of neighboring boxes by coord tuples
            for pair in surrounding:
                # Add to the total number of neighbors
                total[self.boxes[key][COLOR_INDEX]] += 1
                if self.boxes[pair][COLOR_INDEX] == self.boxes[key][COLOR_INDEX]:
                    each[self.boxes[key][COLOR_INDEX]] += 1

            

        return each, total

    def analyze_totals(self):
        each = [0 for i in range(8)]
        total = 0

        for key in self.boxes:
            color_int = self.boxes[key][COLOR_INDEX]
            if color_int == INIT_BLACK:
                continue
            else:
                total += 1
                each[color_int] += 1
        
        return each, total


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