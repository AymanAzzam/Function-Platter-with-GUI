import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QTimer


class CanvasFigure(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot()
        super(CanvasFigure, self).__init__(self.fig)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # set a Title
        self.setWindowTitle("Function Plotter")

        # Create Widgets
        self.__create_widgets()

        # Get initial plot
        self.graph = self.figure.axes.plot([], [])[0]

        # Create Layout and Add Widgets
        self.__create_layout()

        # Change Style
        self.__change_style()

        # Connect the button to a function
        self.button.clicked.connect(self.__update)

    def __create_widgets(self):

        # Tha Main Widgets
        self.function = QLineEdit("x^2")
        self.x_min = QLineEdit("-10")
        self.x_max = QLineEdit("20")
        self.button = QPushButton("Draw")

        self.figure = CanvasFigure()

        # Labels
        self.function_label = QLabel("F(x)")  # Label for the function
        self.x_min_label = QLabel("Xmin")  # Label for the X minimum
        self.x_max_label = QLabel("Xmax")  # label for the X maximum
        # Label for Messages to user
        self.result_label = QLabel("\nWrite your function then press Draw\n")

    def __change_style(self):

        # Style for the Window
        self.setStyleSheet("background-color: darkcyan;")

        # Style for the message to user
        user_message = "border :3px solid black; background-color: yellow; font: bold 16pt;"
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(user_message)

        # Style for the Edited Texts
        style_sheet_edit = "background-color: white;"
        self.function.setStyleSheet(style_sheet_edit)
        self.x_min.setStyleSheet(style_sheet_edit)
        self.x_max.setStyleSheet(style_sheet_edit)

        # Style for the Labels
        style_sheet_label = "font: bold; color: white"
        self.function_label.setStyleSheet(style_sheet_label)
        self.x_min_label.setStyleSheet(style_sheet_label)
        self.x_max_label.setStyleSheet(style_sheet_label)

    def __create_layout(self):

        # Create Grid Layout
        self.layout = QGridLayout()

        # the first row
        self.layout.addWidget(self.function_label, 0, 0, 1, 1)
        self.layout.addWidget(self.function, 0, 1, 1, 3)

        # the second row
        self.layout.addWidget(self.x_min_label, 1, 0)
        self.layout.addWidget(self.x_min, 1, 1)
        self.layout.addWidget(self.x_max_label, 1, 2)
        self.layout.addWidget(self.x_max, 1, 3)

        # the third Row
        self.layout.addWidget(self.button, 2, 0, 1, 4)

        # the fourth Row
        self.layout.addWidget(self.figure, 3, 0, 1, 4)

        # the fifth Row
        self.layout.addWidget(self.result_label, 4, 0, 1, 4)

        # Set the layout
        self.setLayout(self.layout)

    def __update(self):
        # Validate the user Inputs
        x_min, x_max, fx, err = self.__validate_inputs()

        # return if there is an error
        if err:
            QTimer.singleShot(2500, self.__update_message)
            return

        # Solving the division by zero problem
        samples = 500
        threshold = 0.000000101
        x = np.linspace(x_min - threshold, x_max + threshold, samples)
        y = eval(fx)

        # Solve constant Function
        try:
            len(y)
        except:
            y = np.full(len(x), y)

        # Update the data
        self.graph.set_data(x, y)

        # Limit the x-axis & y-yaxis
        threshold2 = 1
        y_min = min(y)
        y_max = max(y)
        plt.xlim(x_min - threshold2, x_max + threshold2)
        plt.ylim(y_min - threshold2, y_max + threshold2)

        # Apply the Updates
        self.figure.fig.canvas.draw()

    # update the user message after invalid input
    def __update_message(self):
        self.result_label.setText(self.user_message)

    def __validate_inputs(self):

        # Get the user inputs
        x_min_string = str(self.x_min.text())
        x_max_string = str(self.x_max.text())
        fx = str(self.function.text())
        fx_string = fx.replace("^", "**")

        # Check the function validation
        x = 0.010111
        try:
            eval(fx_string)
        except:
            self.user_message = self.result_label.text()
            message = "\nError: Function Expression is invalid \n"
            self.result_label.setText(message)
            return 0, 0, "", 1

        # Check X_min and X_max are numbers
        try:
            x_min = float(x_min_string)
            x_max = float(x_max_string)
        except:
            self.user_message = self.result_label.text()
            message = "\nError: Xmin & Xmax must be numbers\n"
            self.result_label.setText(message)
            return 0, 0, "", 1

        # Check X_max > X_min
        if x_min >= x_max:
            self.user_message = self.result_label.text()
            message = "\nError: Xmax must be greater than Xmin\n"
            self.result_label.setText(message)
            return 0, 0, "", 1

        message = "\n y = " + fx + " ,   x = [" + x_min_string + ", " + x_max_string + "]\n"
        self.user_message = message
        self.result_label.setText(message)

        return x_min, x_max, fx_string, 0


if __name__ == "__main__":

    # Create the QT Application
    app = QApplication(sys.argv)

    # Create a window and show it
    window = Form()
    window.show()

    # Run the QT Application
    sys.exit(app.exec_())
