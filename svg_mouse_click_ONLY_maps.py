from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtXml import *
from PyQt5.QtSvg import *

COLOUR_MAP = {
    "p1": Qt.cyan,
    "p2": Qt.red,
    "p3": Qt.green,
    "p4": Qt.red,
    "p5": Qt.green,
    "default": Qt.blue,
}

STATES = {
    "p1": "p1 state changed",
    "p2": "p2 state changed",
    "p3": "p3 state changed",
    "p4": "p4 state changed",
    "p5": "p5 state changed",
}


class SvgItem(QGraphicsSvgItem):
    def __init__(self, id, renderer, parent=None):
        super().__init__(parent)
        self.id = id

        self.setSharedRenderer(renderer)

        self.setElementId(id)
        bounds = renderer.boundsOnElement(id)
        self.setPos(bounds.topLeft())

        self.setFlag(self.ItemIsSelectable)  # horrible selection-box
        self.setFlag(self.ItemIsMovable)

        self.effect = QGraphicsColorizeEffect()

        # create an image based on theC item size
        img = QImage(bounds.size().toSize(), QImage.Format_ARGB32)
        # clear its buffer (this is important!)
        img.fill(Qt.transparent)
        # create a qpainter and ask the renderer to render it
        qp = QPainter(img)
        renderer.render(qp, id)
        qp.end()

        # create the mask by adding a QRegion based on it
        mask = img.createAlphaMask()
        shape = QPainterPath()
        shape.addRegion(QRegion(QBitmap.fromImage(mask)))
        # a QBitmap based region can be unnecessarily complex, let's
        # simplify it
        self._shape = shape.simplified()

    def shape(self):
        return self._shape

    def paint(self, qp, option, widget):
        # keep track of the selected state and call the base painting
        # implementation without it
        selected = option.state & QStyle.State_Selected
        option.state &= ~QStyle.State_Selected
        super().paint(qp, option, widget)

        if selected:
            # draw the selection based on the shape, using the right
            # amount of contrast with the background
            fgcolor = option.palette.windowText().color()
            bgcolor = QColor(
                0 if fgcolor.red() > 127 else 255,
                0 if fgcolor.green() > 127 else 255,
                0 if fgcolor.blue() > 127 else 255,
            )

            qp.setPen(QPen(bgcolor, 0, Qt.SolidLine))
            qp.setBrush(Qt.NoBrush)
            qp.drawPath(self._shape)

            qp.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
            qp.setBrush(Qt.NoBrush)
            qp.drawPath(self._shape)

    def change_state_by_id(self, _id):
        # This will need to be run inside a QThread or QAsync (seperate module)
        # this method will prepare the thread and send any required variables.
        # Create any `handler` methods for any signals emitted from the thread.
        print(STATES[_id])

    def change_colour_by_id(self, col):
        print(self.effect.color() == col)
        if self.effect.color() == col:
            col = COLOUR_MAP["default"]
        self.effect.setColor(col)
        self.setGraphicsEffect(self.effect)

    def mousePressEvent(self, event: "QtWidgets.QGraphicsSceneMouseEvent"):
        print("svg item: " + self.id + " - mousePressEvent()")
        self.change_colour_by_id(COLOUR_MAP[self.id])
        self.change_state_by_id(self.id)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent"):
        print("svg item: " + self.id + " - mouseReleaseEvent()")
        super().mouseReleaseEvent(event)


class SvgViewer(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self._renderer = QSvgRenderer()
        self.setScene(self._scene)

    def set_svg(self, data):
        self.resetTransform()
        self._scene.clear()
        self._renderer.load(data)

        for state_name in STATES.keys():
            item = SvgItem(state_name, self._renderer)
            self._scene.addItem(item)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.viewer = SvgViewer(self)
        vb_layout = QVBoxLayout(self)
        vb_layout.addWidget(self.viewer)
        self.img = "test.svg"
        self.viewer.set_svg(self.img)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())
