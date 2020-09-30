from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsScene

from shibumi.spargo.display import SpargoDisplay
from shibumi.spargo.game import SpargoState
from tests.spline.test_spline_display import add_text, trigger_resize
from zero_play.pixmap_differ import PixmapDiffer


def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spargo_empty') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SpargoDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SpargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        small_black = SpargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                                QSize(30, 30))
        small_white = SpargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                                QSize(30, 30))

        expected_scene.addPixmap(black_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.addPixmap(small_black).setPos(240, 26)
        expected_scene.addPixmap(small_white).setPos(270, 26)
        add_text(expected_scene, '0', 255, 65, 11)
        add_text(expected_scene, '0', 285, 65, 11)
        expected_scene.render(expected)

        display = SpargoDisplay()

        trigger_resize(display, 300, 240)

        display.scene().render(actual)


# noinspection DuplicatedCode
def test_update(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spargo_update') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SpargoDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SpargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        white_ball = SpargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        small_black = SpargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                                QSize(30, 30))
        small_white = SpargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                                QSize(30, 30))

        expected_scene.addPixmap(black_ball).setPos(63, 166)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.addPixmap(small_black).setPos(240, 26)
        expected_scene.addPixmap(small_white).setPos(270, 26)
        add_text(expected_scene, '1', 255, 65, 11)
        add_text(expected_scene, '0', 285, 65, 11)
        expected_scene.render(expected)

        display = SpargoDisplay()

        trigger_resize(display, 300, 240)
        display.update_board(SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
>W
"""))

        display.scene().render(actual)
