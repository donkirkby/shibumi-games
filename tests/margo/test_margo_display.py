from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter, QPixmap, Qt
from PySide2.QtWidgets import QGraphicsScene

from shibumi.margo.display import MargoDisplay
from shibumi.spargo.game import SpargoState
from tests.spline.test_spline_display import trigger_resize, add_text
from zero_play.pixmap_differ import PixmapDiffer


# noinspection DuplicatedCode
def test_board_size_2(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(360, 240, 'margo_board_size_2') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 360, 240)
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
        board_item.setPos(1, 0)
        white_ball = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(103, 103))
        black_ball = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(103, 103))
        black_player = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                                QSize(59, 59))
        mini_white = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(29, 29))
        mini_black = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(29, 29))

        expected_scene.addPixmap(white_ball).setPos(20, 108)
        expected_scene.addPixmap(black_ball).setPos(110, 18)
        expected_scene.addPixmap(black_player).setPos(234, 88)
        expected_scene.addPixmap(mini_black).setPos(234, 25)
        expected_scene.addPixmap(mini_white).setPos(263, 25)
        add_text(expected_scene, '1', 249, 63, 11)
        add_text(expected_scene, '1', 278, 63, 11)
        add_text(expected_scene, 'to move', 263, 155, 11)
        expected_scene.render(expected)

        display = MargoDisplay(size=2)

        trigger_resize(display, 292, 240)
        board_text = """\
  A C
3 . B 3

1 W . 1
  A C
>B
"""
        display.update_board(SpargoState(board_text, size=2))

        display.scene().render(actual)


# noinspection DuplicatedCode
def test_board_size_3(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(360, 240, 'margo_board_size_3') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 360, 240)
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
        scaled_board = assembled_board.scaled(233, 238,
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
        board_item = expected_scene.addPixmap(scaled_board)
        board_item.setPos(-1, 2)
        white_ball = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(75, 75))
        black_ball = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(75, 75))
        black_player = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                                QSize(59, 59))
        mini_white = MargoDisplay.load_pixmap('ball-w-shadow-1.png',
                                              QSize(29, 29))
        mini_black = MargoDisplay.load_pixmap('ball-b-shadow-1.png',
                                              QSize(29, 29))

        expected_scene.addPixmap(white_ball).setPos(12, 145)
        expected_scene.addPixmap(black_ball).setPos(77, 80)
        expected_scene.addPixmap(black_player).setPos(234, 89)
        expected_scene.addPixmap(mini_black).setPos(234, 27)
        expected_scene.addPixmap(mini_white).setPos(264, 27)
        add_text(expected_scene, '1', 249, 66, 11)
        add_text(expected_scene, '1', 278, 66, 11)
        add_text(expected_scene, 'to move', 263, 155, 11)
        expected_scene.render(expected)

        display = MargoDisplay(size=3)

        trigger_resize(display, 292, 240)
        board_text = """\
  A C E
5 . . . 5

3 . B . 3

1 W . . 1
  A C E
>B
"""
        display.update_board(SpargoState(board_text, size=3))

        display.scene().render(actual)


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
        black_player = display.scale_pixmap(display.black_pixmap, 47, 47)
        expected_scene.addPixmap(black_player).setPos(268, 71)
        small_black = display.scale_pixmap(display.black_pixmap, 23, 23)
        expected_scene.addPixmap(small_black).setPos(269, 20)
        small_white = display.scale_pixmap(display.white_pixmap, 23, 23)
        expected_scene.addPixmap(small_white).setPos(292, 20)
        add_text(expected_scene, '0', 280, 50, 9)
        add_text(expected_scene, '0', 304, 50, 9)
        add_text(expected_scene, 'to move', 292, 124, 9)
        add_text(expected_scene, '3', 57, 57, 12)
        add_text(expected_scene, '2', 68, 93, 12)
        add_text(expected_scene, '1', 57, 129, 12)
        add_text(expected_scene, 'A', 141, 214, 12)
        add_text(expected_scene, 'B', 177, 203, 12)
        add_text(expected_scene, 'C', 213, 214, 12)
        expected_scene.render(expected)

        trigger_resize(display, 360, 240)
        display.show_coordinates = True
        # display.move_text.setText(f'{display.text_y}')

        display.scene().render(actual)
