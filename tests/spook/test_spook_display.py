from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsScene

from shibumi.spook.display import SpookDisplay
from shibumi.spook.state import SpookState
from zero_play.pixmap_differ import PixmapDiffer, render_display


# noinspection DuplicatedCode
def test_hover_enter_remove(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240,
                                       'spook_hover_enter_remove') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SpookDisplay.load_pixmap('board-1.png',
                                     QSize(240, 240))).setPos(1, 0)
        white_ball = SpookDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(60, 60))
        red_ball = SpookDisplay.load_pixmap('ball-r-shadow-1.png',
                                            QSize(60, 60))
        black_ball = SpookDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(60, 60))

        black_piece = expected_scene.addPixmap(black_ball)
        black_piece.setPos(115, 114)
        black_piece.setOpacity(0.5)
        red_piece = expected_scene.addPixmap(red_ball)
        red_piece.setPos(63, 62)
        white_piece = expected_scene.addPixmap(white_ball)
        white_piece.setPos(115, 62)
        expected_scene.render(expected)

        display = SpookDisplay()
        display.update_board(SpookState('''\
  A C E G
7 . . . . 7

5 . R W . 5

3 . . B . 3

1 . . . . 1
  A C E G
>R(R,B)
'''))
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(348, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)

        render_display(display, actual)
