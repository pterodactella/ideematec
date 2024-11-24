import json
from PySide6 import QtWidgets, QtCore, QtGui
from canvas import Canvas
from models import Channel, DrawnShape, Square
from drawing import ShapeDrawer


class ControlPanel(QtWidgets.QWidget):
    def __init__(self, canvas):
        super(ControlPanel, self).__init__()
        self.canvas: Canvas = canvas
        self.shape_drawer = ShapeDrawer(self.canvas.scene)
        self.init_ui()

    def init_ui(self):
        """
        This function sets up the control widgets: dropdown with the shapes,
        input fields and button to save the shape information.
        """
        # Create drop-downs
        shape_dropdown_label = QtWidgets.QLabel("Shape:")
        self.shape_dropdown = QtWidgets.QComboBox()
        self.shape_dropdown.addItems(["SQR", "U"])

        # Create input fields
        self.side_label = QtWidgets.QLabel("Side:")
        self.side_input = QtWidgets.QLineEdit()
        self.side_input.setValidator(self.format_input())
        self.side_input.textChanged.connect(self.update_shape)

        self.height_label = QtWidgets.QLabel("Height:")
        self.height_input = QtWidgets.QLineEdit()
        self.height_input.setValidator(self.format_input())
        self.height_input.textChanged.connect(self.update_shape)

        self.height_label.setVisible(False)
        self.height_input.setVisible(False)

        self.width_label = QtWidgets.QLabel("Width:")
        self.width_input = QtWidgets.QLineEdit()
        self.width_input.setValidator(self.format_input())
        self.width_input.textChanged.connect(self.update_shape)

        self.width_label.setVisible(False)
        self.width_input.setVisible(False)

        self.thickness_label = QtWidgets.QLabel("Thickness:")
        self.thickness_input = QtWidgets.QLineEdit()
        self.thickness_input.setValidator(self.format_input())
        self.thickness_input.textChanged.connect(self.update_shape)

        # Conditionally render the fields
        self.shape_dropdown.currentIndexChanged.connect(self.conditional_rendering)
        self.shape_dropdown.currentIndexChanged.connect(self.update_shape)
        self.conditional_rendering()

        # Add the save button
        draw_button = QtWidgets.QPushButton("Save Shape")
        draw_button.clicked.connect(self.draw_shape)

        # Add labels
        form = QtWidgets.QFormLayout()
        form.addRow(shape_dropdown_label, self.shape_dropdown)
        form.addRow(self.side_label, self.side_input)
        form.addRow(self.height_label, self.height_input)
        form.addRow(self.width_label, self.width_input)
        form.addRow(self.thickness_label, self.thickness_input)
        form.addRow(draw_button)

        self.setLayout(form)

    def conditional_rendering(self):
        """
        Create mapping of input field for given shape
        """
        field_visibility = {
            "SQR": {"side": True, "height": False, "width": False},
            "U": {"side": False, "height": True, "width": True},
        }

        visibility = field_visibility.get(self.shape_dropdown.currentText(), {})
        self.side_label.setVisible(visibility.get("side", False))
        self.side_input.setVisible(visibility.get("side", False))
        self.height_label.setVisible(visibility.get("height", False))
        self.height_input.setVisible(visibility.get("height", False))
        self.width_label.setVisible(visibility.get("width", False))
        self.width_input.setVisible(visibility.get("width", False))

    def update_shape(self):
        """
        Updates the shape dynamically based on user input.
        """
        self.canvas.clear_scene()

        # Get inputs
        shape_type = self.shape_dropdown.currentText()
        thickness = self.thickness_input.text()

        if shape_type == "SQR":
            # get the side length
            side = float(self.side_input.text())
            self.shape_drawer.draw_shape(
                DrawnShape(shape=Square(side=side), thickness=thickness)
            )
        else:
            # get height and width
            height = float(self.height_input.text())
            width = float(self.width_input.text())
            self.shape_drawer.draw_shape(
                DrawnShape(
                    shape=Channel(height=height, width=width), thickness=thickness
                )
            )

    def draw_shape(self):
        """
        This function draws the shapes depending on the user selection
        """
        shape_type = self.shape_dropdown.currentText()
        thickness = self.thickness_input.text()
        if not thickness:
            return

        try:
            thickness = float(thickness)
        except ValueError:
            return

        if shape_type == "SQR":
            side = float(self.side_input.text())
            square = Square(side=side)
            drawn_shape = DrawnShape(shape=square, thickness=thickness)
        elif shape_type == "U":
            height = float(self.height_input.text())
            width = float(self.width_input.text())
            drawn_shape = DrawnShape(
                shape=Channel(height=height, width=width), thickness=thickness
            )

        # Draw and save
        self.canvas.clear_scene()
        self.shape_drawer.draw_shape(drawn_shape)
        self.save_shape(drawn_shape)

    def save_shape(self, shape: DrawnShape):
        """
        This function saves the DrawnShape model inside a json file.
        """
        array = shape.to_array()
        try:
            with open("store.json", "r") as f:
                shapes = json.load(f) or {}
        except (FileNotFoundError, json.JSONDecodeError):
            shapes = {}

        # Increment the shape key
        shapes[f"Shape_{len(shapes) + 1}"] = array
        print(shapes)
        with open("store.json", "w") as f:
            json.dump(shapes, f, indent=4)

    def format_input(self):
        """
        When having a field in and out of focus the value would get rewritten
        in a scientific notation, this function insures consistent formatting.
        The locale configuration can be changed.
        """
        validator = QtGui.QDoubleValidator(0.0, 1000.0, 2)
        validator.setLocale(
            QtCore.QLocale(
                QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedKingdom
            )
        )
        validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        return validator


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
