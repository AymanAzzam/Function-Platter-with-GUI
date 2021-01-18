import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt 

class CanvasFigure(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(CanvasFigure, self).__init__(self.fig)

class Form(QDialog):

    def __init__(self,parent = None):
        super(Form, self).__init__(parent)

        ##########          set a Title         ##########
        self.setWindowTitle("Function Plotter")

        ##########          Create Widgets          ##########
        self.__CreateWidgets()

        ##########          Change Style            ##########
        self.__ChangeStyle()

        ##########          Get initial plot        ##########
        self.graph = self.sc.axes.plot([], [])[0]

        ##########  Create Layout and Add Widgets   ##########
        self.__CraeteLayout()
        
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
        self.function_label = QLabel("y   =")               # Label for the function
        self.x_min_label = QLabel("Xmin   =")               # Label for the X minium
        self.x_max_label = QLabel("Xmax   =")               # label for the X maximum
        # Label for Messages to user
        self.result_label = QLabel("\nWrite your function then press Draw\n")    
        

    def __ChangeStyle(self):
        
        ## Style for message to user
        font = QFont("Arial", 16, QFont.Bold)
        self.result_label.setFont(font)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border :3px solid black;")
        
        ## Style for The button
        #self.button.setStyleSheet("padding :15px")

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
        xmin,xmax,fx,err = self.__ValidateInputs()
        
        ## return if there is an error
        if err:
            return

        ## Update the data
        x = np.linspace(xmin,xmax)
        y = eval(fx)
        self.graph.set_data(x,y)

        ## Limit the x-axis & y-yaxis
        ymin = min(y)
        ymax = max(y)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)
        
        ## Apply the Updates
        self.sc.fig.canvas.draw()

    def __ValidateInputs(self):
        
        ## Get the user inputs
        xmin_string = str(self.x_min.text())
        xmax_string = str(self.x_max.text())
        fx_string = str(self.function.text()).replace("^","**")

        ## Check the function validation
        x = 0
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

        message = "\nSuccessful Drawing\n"
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