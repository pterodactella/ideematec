import json
from PySide6 import QtWidgets, QtCore, QtGui
from canvas import Canvas
from models import Channel, DrawnShape, Square


class ControlPanel(QtWidgets.QWidget):
    def __init__(self, canvas):
        super(ControlPanel, self).__init__()
        self.canvas = canvas
        self.init_ui()

    def init_ui(self):
        # Create drop-down menu for choosing the shape
        shape_dropdown_label = QtWidgets.QLabel("Shape:")
        self.shape_dropdown = QtWidgets.QComboBox()
        self.shape_dropdown.addItems(["SQR", "U"])

        # Create Input fields for each shape
        self.side_label = QtWidgets.QLabel("Side:")
        self.side_input = QtWidgets.QLineEdit()
        self.side_input.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2))
        self.side_input.editingFinished.connect(
            lambda: self.format_input(self.side_input)
        )

        self.height_label = QtWidgets.QLabel("Height:")
        self.height_input = QtWidgets.QLineEdit()
        self.height_input.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2))
        self.height_input.editingFinished.connect(
            lambda: self.format_input(self.height_input)
        )
        self.height_label.setVisible(False)
        self.height_input.setVisible(False)

        self.width_label = QtWidgets.QLabel("Width:")
        self.width_input = QtWidgets.QLineEdit()
        self.width_input.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2))
        self.width_input.editingFinished.connect(
            lambda: self.format_input(self.width_input)
        )
        self.width_label.setVisible(False)
        self.width_input.setVisible(False)

        self.thickness_label = QtWidgets.QLabel("Thickness:")
        self.thickness_input = QtWidgets.QLineEdit()
        self.thickness_input.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2))
        self.thickness_input.editingFinished.connect(
            lambda: self.format_input(self.thickness_input)
        )

        # Function to update input fields based on dropdown selection
        self.shape_dropdown.currentIndexChanged.connect(self.conditional_rendering)

        # Call the function once to set the initial state
        self.conditional_rendering()

        # Add a button to draw the shape
        draw_button = QtWidgets.QPushButton("Draw Shape")
        draw_button.clicked.connect(self.draw_shape)

        # Add the label and component in a form layout
        form = QtWidgets.QFormLayout()
        form.addRow(shape_dropdown_label, self.shape_dropdown)
        form.addRow(self.side_label, self.side_input)
        form.addRow(self.height_label, self.height_input)
        form.addRow(self.width_label, self.width_input)
        form.addRow(self.thickness_label, self.thickness_input)
        form.addRow(draw_button)

        self.setLayout(form)

    def conditional_rendering(self):
        shape_type = self.shape_dropdown.currentText()
        if shape_type == "SQR":
            self.side_label.setVisible(True)
            self.side_input.setVisible(True)
            self.height_label.setVisible(False)
            self.height_input.setVisible(False)
            self.width_label.setVisible(False)
            self.width_input.setVisible(False)
        elif shape_type == "U":
            self.side_label.setVisible(False)
            self.side_input.setVisible(False)
            self.height_label.setVisible(True)
            self.height_input.setVisible(True)
            self.width_label.setVisible(True)
            self.width_input.setVisible(True)

    def draw_shape(self):
        self.canvas.clear_scene()

        shape_type = self.shape_dropdown.currentText()
        thickness = float(self.thickness_input.text())

        if shape_type == "SQR":
            side = float(self.side_input.text())
            square = Square(side=side)
            drawn_shape = DrawnShape(shape=square, thickness=thickness)
        elif shape_type == "U":
            height = float(self.height_input.text())
            width = float(self.width_input.text())
            channel = Channel(height=height, width=width)
            drawn_shape = DrawnShape(shape=channel, thickness=thickness)

        self.canvas.shape_drawer.draw_shape(drawn_shape)
        self.save_shape(drawn_shape)

    def save_shape(self, shape: DrawnShape):
        array = shape.to_array()
        try:
            with open("store.json", "r") as f:
                shapes = json.load(f) or {}
        except (FileNotFoundError, json.JSONDecodeError):
            shapes = {}

        # increment the shape key
        shapes[f"Shape_{len(shapes) + 1}"] = array
        print(shapes)
        with open("store.json", "w") as f:
            json.dump(shapes, f, indent=4)

    # One of the issues that i noticed was that when having a field in and out of focus the value would get rewritten in a scientific notation, that why we have this function.
    def format_input(self, line_edit):
        value = line_edit.text()
        if value:
            line_edit.setText(f"{float(value):.2f}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    canvas = Canvas()
    window.setCentralWidget(canvas)

    # Create and add the control panel
    control_panel = ControlPanel(canvas)
    dock_widget = QtWidgets.QDockWidget("Controls", window)
    dock_widget.setWidget(control_panel)
    window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)

    window.show()
    app.exec()
