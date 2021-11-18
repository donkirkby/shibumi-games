from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QPixmap, Qt
from PySide6.QtWidgets import QGraphicsScene

from shibumi.margo.display import MargoDisplay
from shibumi.spargo.game import SpargoState
from tests.spline.test_spline_display import trigger_resize, add_text
from zero_play.pixmap_differ import PixmapDiffer, render_display


# noinspection DuplicatedCode
def test_board_size_2(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'margo_board_size_2') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        full_board = MargoDisplay.load_pixmap('board-1.png')
        width = full_board.width()
        height = full_board.height()
        top_height = round(height * 0.28)
        left_width = round(width * 0.28)
        right_width = round(width * 0.279)
        bottom_height = round(height * 0.29)
        assembled_board = QPixmap(left_width+right_width,
                                  top_height+bottom_height)
        assembled_board.fill(Qt.transparent)
        assembled_painter = QPainter(assembled_board)
        # top left
        assembled_painter.drawPixmap(0, 0,
                                     left_width, top_height,
                                     full_board,
                                     0, 0,
                                     left_width, top_height)
        # top right
        assembled_painter.drawPixmap(left_width, 0,
                                     right_width, top_height,
                                     full_board,
                                     width-right_width, 0,
                                     right_width, top_height)
        # bottom left
        assembled_painter.drawPixmap(0, top_height,
                                     left_width, bottom_height,
                                     full_board,
                                     0, height-bottom_height,
                                     left_width, bottom_height)
        # bottom right
        assembled_painter.drawPixmap(left_width, top_height,
                                     right_width, bottom_height,
                                     full_board,
                                     width-right_width, height-bottom_height,
                                     right_width, bottom_height)
        assembled_painter.end()
        scaled_board = assembled_board.scaled(232, 240,
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
        board_item = expected_scene.addPixmap(scaled_board)
        board_item.setPos(4, 0)
        white_ball = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(103, 103))
        black_ball = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(103, 103))

        expected_scene.addPixmap(white_ball).setPos(23, 108)
        expected_scene.addPixmap(black_ball).setPos(113, 18)
        expected_scene.render(expected)

        display = MargoDisplay(size=2)

        trigger_resize(display, 292, 240)
        display.resize(348, 264)
        board_text = """\
  A C
3 . B 3

1 W . 1
  A C
>B
"""
        display.update_board(SpargoState(board_text, size=2))

        render_display(display, actual)


# noinspection DuplicatedCode
def test_board_size_3(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'margo_board_size_3') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        full_board = MargoDisplay.load_pixmap('board-1.png')
        width = full_board.width()
        height = full_board.height()
        top_height = round(height * 0.28)
        mid_height = round(height * 0.21)
        bottom_height = round(height * 0.29)
        left_width = round(width * 0.28)
        mid_width = round(width * 0.22)
        right_width = round(width * 0.279)
        assembled_board = QPixmap(left_width+mid_width+right_width,
                                  top_height+mid_height+bottom_height)
        assembled_board.fill(Qt.transparent)
        assembled_painter = QPainter(assembled_board)
        # top left
        assembled_painter.drawPixmap(0, 0,
                                     left_width, top_height,
                                     full_board,
                                     0, 0,
                                     left_width, top_height)
        # top middle
        assembled_painter.drawPixmap(left_width, 0,
                                     mid_width, top_height,
                                     full_board,
                                     left_width, 0,
                                     mid_width, top_height)
        # top right
        assembled_painter.drawPixmap(left_width+mid_width, 0,
                                     right_width, top_height,
                                     full_board,
                                     width-right_width, 0,
                                     right_width, top_height)
        # left middle
        assembled_painter.drawPixmap(0, top_height,
                                     left_width, mid_height,
                                     full_board,
                                     0, top_height,
                                     left_width, mid_height)
        # middle middle
        assembled_painter.drawPixmap(left_width, top_height,
                                     mid_width, mid_height,
                                     full_board,
                                     left_width, top_height,
                                     mid_width, mid_height)
        # right middle
        assembled_painter.drawPixmap(left_width+mid_width, top_height,
                                     right_width, mid_height,
                                     full_board,
                                     width-right_width, top_height,
                                     right_width, mid_height)
        # bottom left
        assembled_painter.drawPixmap(0, top_height+mid_height,
                                     left_width, bottom_height,
                                     full_board,
                                     0, height-bottom_height,
                                     left_width, bottom_height)
        # bottom middle
        assembled_painter.drawPixmap(left_width, top_height+mid_height,
                                     mid_width, bottom_height,
                                     full_board,
                                     left_width, height-bottom_height,
                                     mid_width, bottom_height)
        # bottom right
        assembled_painter.drawPixmap(left_width+mid_width, top_height+mid_height,
                                     right_width, bottom_height,
                                     full_board,
                                     width-right_width, height-bottom_height,
                                     right_width, bottom_height)
        assembled_painter.end()
        scaled_board = assembled_board.scaled(240, 240,
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
        board_item = expected_scene.addPixmap(scaled_board)
        board_item.setPos(2, 0)
        white_ball = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(76, 76))
        black_ball = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(76, 76))

        expected_scene.addPixmap(white_ball).setPos(15, 145)
        expected_scene.addPixmap(black_ball).setPos(81, 79)
        expected_scene.render(expected)

        display = MargoDisplay(size=3)
        display.resize(348, 264)

        board_text = """\
  A C E
5 . . . 5

3 . B . 3

1 W . . 1
  A C E
>B
"""
        display.update_board(SpargoState(board_text, size=3))

        render_display(display, actual)


# noinspection DuplicatedCode
def test_coordinates(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(360, 240, 'margo_coordinates') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 360, 240)
        display = MargoDisplay(size=2)
        full_board = display.assemble_board()
        scaled_board = display.scale_pixmap(full_board, 185, 192)
        expected_scene.addPixmap(scaled_board).setPos(82, 0)
        add_text(expected_scene, '3', 57, 57, 12)
        add_text(expected_scene, '2', 68, 93, 12)
        add_text(expected_scene, '1', 57, 129, 12)
        add_text(expected_scene, 'A', 141, 214, 12)
        add_text(expected_scene, 'B', 177, 203, 12)
        add_text(expected_scene, 'C', 213, 214, 12)
        expected_scene.render(expected)

        display.resize(492, 264)

        display.show_coordinates = True

        render_display(display, actual)
