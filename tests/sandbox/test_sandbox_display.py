from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter, QColor, QPainterPath
from PySide2.QtWidgets import QGraphicsScene, QApplication

from shibumi.sandbox.display import SandboxDisplay
from shibumi.sandbox.game import SandboxState
from tests.spline.test_spline_display import add_text, trigger_resize
from zero_play.pixmap_differ import PixmapDiffer


# noinspection DuplicatedCode
def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'sandbox_empty') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        small_black = SandboxDisplay.load_pixmap('ball-b-shadow-1.png',
                                                 QSize(30, 30))
        small_white = SandboxDisplay.load_pixmap('ball-w-shadow-1.png',
                                                 QSize(30, 30))

        expected_scene.addPixmap(small_black).setPos(240, 26)
        expected_scene.addPixmap(small_white).setPos(270, 26)
        add_text(expected_scene, '0', 255, 65, 11)
        add_text(expected_scene, '0', 285, 65, 11)
        path = QPainterPath()
        path.addRoundedRect(240, 180, 29, 29, 3, 3)
        expected_scene.addPath(path, brush=QColor('blue'))
        expected_scene.addPixmap(small_black).setPos(240, 180)
        expected_scene.addPixmap(small_white).setPos(270, 180)

        expected_scene.render(expected)

        display = SandboxDisplay()

        trigger_resize(display, 300, 240)

        display.scene().render(actual)


# noinspection DuplicatedCode
def test_selected_colour(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'sandbox_selected_colour') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        small_black = SandboxDisplay.load_pixmap('ball-b-shadow-1.png',
                                                 QSize(30, 30))
        small_white = SandboxDisplay.load_pixmap('ball-w-shadow-1.png',
                                                 QSize(30, 30))

        expected_scene.addPixmap(small_black).setPos(240, 26)
        expected_scene.addPixmap(small_white).setPos(270, 26)
        add_text(expected_scene, '0', 255, 65, 11)
        add_text(expected_scene, '0', 285, 65, 11)
        path = QPainterPath()
        path.addRoundedRect(270, 180, 29, 29, 3, 3)
        expected_scene.addPath(path, brush=QColor('blue'))
        expected_scene.addPixmap(small_black).setPos(240, 180)
        expected_scene.addPixmap(small_white).setPos(270, 180)

        expected_scene.render(expected)

        display = SandboxDisplay()

        trigger_resize(display, 300, 240)
        display.selected_colour = SandboxState.WHITE

        display.scene().render(actual)


def test_make_move(application: QApplication):
    expected_text = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . W . 1
  A C E G
"""
    display = SandboxDisplay()
    display.selected_colour = SandboxState.WHITE

    display.make_move(2)

    assert display.current_state.display() == expected_text
