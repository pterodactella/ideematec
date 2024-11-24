from PySide6 import QtWidgets, QtCore, QtGui
from drawing import ShapeDrawer

GRID_STEP = 20


class Canvas(QtWidgets.QGraphicsView):
    def __init__(self):
        super(Canvas, self).__init__()
        self.resize(800, 800)
        self.setMinimumSize(600, 600)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.draw_axes()
        self.shape_drawer = ShapeDrawer(self.scene)

    def draw_axes(self):
        """
        This function prepares the canvas by drawing the x and y axis and adding ticks after each 20 pixels.
        """
        self.scene.clear()  # Clear the scene before drawing the axes

        rect = self.viewport().rect()
        self.scene.setSceneRect(rect)

        # Calculate where the center of the view is
        center_x = rect.width() / 2
        center_y = rect.height() / 2

        # Blue color so it doesn't interfere with the light or dark modes in the local setup
        pen = QtGui.QPen(QtCore.Qt.blue)
        pen.setWidth(2)
        grid_pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.PenStyle.DashLine)
        font = QtGui.QFont("Arial", 8)

        # 1 tick every 20 pixels - same as in the case study picture
        for i in range(0, max(rect.width(), rect.height()), GRID_STEP):
            if i < rect.width():
                self.scene.addLine(i, 0, i, rect.height(), grid_pen)
                if i != center_x:
                    text = self.scene.addText(str(int(i - center_x)), font)
                    text.setDefaultTextColor(QtCore.Qt.blue)
                    text.setPos(i - text.boundingRect().width() / 2, center_y + 5)

            if i < rect.height():
                self.scene.addLine(0, i, rect.width(), i, grid_pen)
                if i != center_y:
                    text = self.scene.addText(str(int(center_y - i)), font)
                    text.setDefaultTextColor(QtCore.Qt.blue)
                    text.setPos(center_x + 5, i - text.boundingRect().height() / 2)

        # Draw the axis on top of the grid
        self.scene.addLine(0, center_y, rect.width(), center_y, pen)
        self.scene.addLine(center_x, 0, center_x, rect.height(), pen)

    def clear_scene(self):
        """
        Clears the scene and redraws the axis
        """
        self.scene.clear()
        self.draw_axes()

    def resizeEvent(self, event):
        """
        Allow user to resize the window. Once a resize event happens, a shape would need to be redrawn by the user.
        """
        self.draw_axes()
        super().resizeEvent(event)
