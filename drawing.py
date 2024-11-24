from PySide6 import QtWidgets, QtCore, QtGui
from models import Channel, DrawnShape, Square


class ShapeDrawer:
    def __init__(self, scene: QtWidgets.QGraphicsScene):
        self.scene = scene

    def add_node(
        self,
        x: int,
        y: int,
        diameter: int = 6,
        color: QtCore.Qt.GlobalColor = QtCore.Qt.red,
    ):
        self.scene.addEllipse(
            x - diameter / 2,
            y - diameter / 2,
            diameter,
            diameter,
            QtGui.QPen(color, 1),
            QtGui.QBrush(color),
        )

    def add_edge(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        thickness: float = 1,
        color: QtCore.Qt.GlobalColor = QtCore.Qt.red,
    ):
        self.scene.addLine(
            start_x,
            start_y,
            end_x,
            end_y,
            QtGui.QPen(color, thickness),
        )

    def draw_shape(self, drawn_shape: DrawnShape):
        """
        Draw the deswired shape using nodes and edges. The shapes can
        either be a instance of the Square or the Channel class
        """
        shape = drawn_shape.shape
        thickness = drawn_shape.thickness

        # Calculate the center position
        scene_rect = self.scene.sceneRect()
        center_x = scene_rect.width() / 2
        center_y = scene_rect.height() / 2

        # Determine the dimensions and the x, y position of the shape
        if isinstance(shape, Square):
            width = height = shape.side
        else:
            width = shape.width
            height = shape.height

        x = center_x - width / 2
        y = center_y - height / 2

        # Add the nodes
        nodes = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        ]

        for node in nodes:
            self.add_node(node[0], node[1])

        # Add edges
        for i in range(len(nodes)):
            start_node = nodes[i]
            end_node = nodes[(i + 1) % len(nodes)]

            # Skip the last edge if the shape is a channel
            if isinstance(shape, Channel) and i == len(nodes) - 1:
                continue
            self.add_edge(
                start_node[0], start_node[1], end_node[0], end_node[1], thickness
            )

        self.add_floating_thickness(thickness, x, center_y)

    def add_floating_thickness(self, thickness: float, x: float = 0, y: float = 0):
        """
        Create a floating box with the thickness information. The box is floating and
        it's position is calculated based on the size of the shape.
        """
        thickness = f"T = {thickness}"

        text_item = QtWidgets.QGraphicsTextItem(thickness)
        font = QtGui.QFont()
        font.setBold(True)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QtCore.Qt.white)

        text_rect = text_item.boundingRect()
        rect_item = QtWidgets.QGraphicsRectItem(text_rect)
        rect_item.setBrush(QtGui.QBrush(QtCore.Qt.gray))
        rect_item.setPen(QtGui.QPen(QtCore.Qt.blue, 2))

        # Position the rectangle and text
        rect_item.setPos(x - 100, y + 10)
        text_item.setPos(x - 100, y + 10)

        # Add items to the scene
        self.scene.addItem(rect_item)
        self.scene.addItem(text_item)
