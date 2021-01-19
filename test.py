
from PySide2.QtCore import Qt
import pytest
import program


@pytest.fixture
def app(qtbot):
    window = program.Form()
    qtbot.addWidget(window)
    return window


def test_function_invalid(app, qtbot):
    old_data = app.graph.get_data()
    app.function.setText("x^2+sin(x)")
    qtbot.mouseClick(app.button, Qt.LeftButton)
    message = str(app.result_label.text())
    ## Test user message is presented right
    assert message.count("Error") == 1 and message.count("Function") == 1
    ## Test the plot didn't change
    new_data = app.graph.get_data()
    assert old_data[0].all() == new_data[0].all()
    assert old_data[1].all() == new_data[1].all()


def test_xmin_invalid(app, qtbot):
    old_data = app.graph.get_data()
    app.x_min.setText("125bx")
    qtbot.mouseClick(app.button, Qt.LeftButton)
    message = str(app.result_label.text())
    ## Test user message is presented right
    assert message.count("Error") == 1 and message.count("Xmin") == 1
    ## Test the plot didn't change
    new_data = app.graph.get_data()
    assert old_data[0].all() == new_data[0].all()
    assert old_data[1].all() == new_data[1].all()


def test_xmax_invalid(app, qtbot):
    old_data = app.graph.get_data()
    app.x_max.setText("")
    qtbot.mouseClick(app.button, Qt.LeftButton)
    message = str(app.result_label.text())
    ## Test user message is presented right
    assert message.count("Error") == 1 and message.count("Xmax") == 1
    ## Test the plot didn't change
    new_data = app.graph.get_data()
    assert old_data[0].all() == new_data[0].all()
    assert old_data[1].all() == new_data[1].all()


def test_valid_case(app, qtbot):
    old_data = app.graph.get_data()
    app.function.setText("x^2")
    app.x_min.setText("-10")
    app.x_max.setText("+10")
    qtbot.mouseClick(app.button, Qt.LeftButton)
    message = str(app.result_label.text())
    ## Test user message is presented right
    assert message.count("Error") == 0 and message.count("x^2") == 1
    ## Test the plot changed
    new_data = app.graph.get_data()
    assert old_data[0].any() != new_data[0].any()
    assert old_data[1].any() != new_data[1].any()