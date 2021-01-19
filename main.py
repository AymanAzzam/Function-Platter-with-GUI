import sys
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QTimer

class CanvasFigure(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(CanvasFigure, self).__init__(self.fig)

class Form(QDialog):

    def __init__(self,parent = None):
        super(Form, self).__init__(parent)

        ##########          set a Title             ##########
        self.setWindowTitle("Function Plotter")
    
        ##########          Create Widgets          ##########
        self.__CreateWidgets()
        
        ##########          Get initial plot        ##########
        self.graph = self.sc.axes.plot([], [])[0]

        ##########  Create Layout and Add Widgets   ##########
        self.__CraeteLayout()

        ##########          Change Style            ##########
        self.__ChangeStyle()
        
        ########## Conncet the button to a function ##########
        self.button.clicked.connect(self.Update)
        
    def __CreateWidgets(self):

        ### Tha Main Widgets ###
        self.function = QLineEdit("x^2")
        self.x_min = QLineEdit("-10")
        self.x_max = QLineEdit("20")
        self.button = QPushButton("Draw")
        
        self.sc = CanvasFigure()
        
        ### Labels ###
        self.function_label = QLabel("F(x)")               # Label for the function
        self.x_min_label = QLabel("Xmin")               # Label for the X minium
        self.x_max_label = QLabel("Xmax")               # label for the X maximum
        # Label for Messages to user
        self.result_label = QLabel("\nWrite your function then press Draw\n")    
        

    def __ChangeStyle(self):
        
        ## Style for Window
        self.setStyleSheet("background-color: darkcyan;")
        
        ## Style for message to user
        user_message = "border :3px solid black; background-color: yellow; font: bold 16pt;"
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(user_message)
        
        ## Style for Edited Texts
        style_sheet_edit = "background-color: white;"
        self.function.setStyleSheet(style_sheet_edit)
        self.x_min.setStyleSheet(style_sheet_edit)
        self.x_max.setStyleSheet(style_sheet_edit)

        ## Style for Labels
        style_sheet_label = "font: bold; color: white"
        self.function_label.setStyleSheet(style_sheet_label)
        self.x_min_label.setStyleSheet(style_sheet_label)
        self.x_max_label.setStyleSheet(style_sheet_label)
        

    def __CraeteLayout(self):

        ### Create Grid Layout ###
        self.layout = QGridLayout()
        
        ## the first row
        self.layout.addWidget(self.function_label,0,0,1,1)
        self.layout.addWidget(self.function,0,1,1,3)
        
        ## the second row
        self.layout.addWidget(self.x_min_label,1,0)
        self.layout.addWidget(self.x_min,1,1)
        self.layout.addWidget(self.x_max_label,1,2)
        self.layout.addWidget(self.x_max,1,3)

        ## the third Row
        self.layout.addWidget(self.button,2,0,1,4)
        
        ## the fourth Row
        self.layout.addWidget(self.sc,3,0,1,4)
        
        ## the fifth Row
        self.layout.addWidget(self.result_label,4,0,1,4)

        ## Set the layout
        self.setLayout(self.layout)
        
    def Update(self):
        ## Validate the user Inputs
        self.user_message = self.result_label.text()
        xmin,xmax,fx,err = self.__ValidateInputs()
        
        ## return if there is an error
        if err:
            QTimer.singleShot(2500, self._updateMessage)
            return
        
        ## Solving the division by zero problem
        samples = 500
        threshold = 0.000000101
        x = np.linspace(xmin-threshold,xmax+threshold,samples)
        y = eval(fx)

        ## Solve constant Function
        try:
            len(y)
        except:
            y = np.full(len(x),y)

        ## Update the data
        self.graph.set_data(x,y)
        
        ## Limit the x-axis & y-yaxis
        threshold2 = 1
        ymin = min(y)
        ymax = max(y)
        plt.xlim(xmin-threshold2,xmax+threshold2)
        plt.ylim(ymin-threshold2,ymax+threshold2)
        
        ## Apply the Updates
        self.sc.fig.canvas.draw()

    ## To update the user message after not valid input
    def _updateMessage(self):
        self.result_label.setText(self.user_message)

    def __ValidateInputs(self):
        
        ## Get the user inputs
        xmin_string = str(self.x_min.text())
        xmax_string = str(self.x_max.text())
        fx = str(self.function.text())
        fx_string = fx.replace("^","**")

        ## Check the function validation
        x = 0.010111
        try:
            eval(fx_string)
        except:
            message = "\nError: Function Expression is invalid \n"
            self.result_label.setText(message)
            return 0,0,"",1

        ## Check Xmin and Xmax are numbers
        try:
            xmin = float(xmin_string)
            xmax = float(xmax_string)
        except:
            message = "\nError: Xmin & Xmax must be numbers\n"
            self.result_label.setText(message)
            return 0,0,"",1

        ## Check Xmax > Xmin     
        if(xmin >= xmax):
            message = "\nError: Xmax must be greater than Xmin\n"
            self.result_label.setText(message)
            return 0,0,"",1

        message = "\n y = " + fx + " ,   x = [" + xmin_string + ", " + xmax_string + "]\n"
        self.result_label.setText(message)
        
        return xmin,xmax,fx_string,0
    
if __name__ == "__main__":
    
    ## Create the QT Apllication
    app = QApplication(sys.argv)
    
    ## Create a window and show it
    window = Form()
    window.show()

    # Run the QT Application
    sys.exit(app.exec_())