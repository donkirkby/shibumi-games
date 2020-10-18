from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsScene

from shibumi.spargo.display import SpargoDisplay
from shibumi.spargo.game import SpargoState
from zero_play.pixmap_differ import PixmapDiffer, render_display


def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'spargo_empty') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SpargoDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)

        expected_scene.render(expected)

        display = SpargoDisplay()
        display.resize(336, 264)

        render_display(display, actual)
    assert display.ui.move_text.text() == 'to move'
    assert display.ui.black_count.text() == '0'
    assert display.ui.white_count.text() == '0'
    black_icon = display.black_pixmap.toImage()
    assert display.ui.black_count_pixmap.pixmap().toImage() == black_icon
    assert display.ui.player_pixmap.pixmap().toImage() == black_icon
    white_icon = display.white_pixmap.toImage()
    assert display.ui.white_count_pixmap.pixmap().toImage() == white_icon


# noinspection DuplicatedCode
def test_update(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'spargo_update') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SpargoDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SpargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(63, 166)
        expected_scene.render(expected)

        display = SpargoDisplay()

        display.resize(336, 264)
        display.update_board(SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
>W
"""))

        render_display(display, actual)
    assert display.ui.black_count.text() == '1'
    assert display.ui.white_count.text() == '0'
