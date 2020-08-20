from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter, QFont
from PySide2.QtWidgets import QGraphicsScene
from zero_play.game_display import center_text_item
from zero_play.pixmap_differ import PixmapDiffer

from shibumi.spline.display import SplineDisplay


def add_text(scene: QGraphicsScene, text: str, x: int, y: int, font_size: int):
    font = QFont(SplineDisplay.default_font)
    font.setPointSize(font_size)
    text_item = scene.addSimpleText(text, font)
    center_text_item(text_item, x, y)


# noinspection DuplicatedCode
def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_empty') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()

        display.resize(QSize(300, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_first_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_first_level') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(white_ball).setPos(11, 10)
        expected_scene.addPixmap(black_ball).setPos(63, 10)
        expected_scene.addPixmap(black_ball).setPos(167, 62)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(QSize(300, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_second_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_second_level') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(11, 62)
        expected_scene.addPixmap(white_ball).setPos(63, 62)
        expected_scene.addPixmap(white_ball).setPos(11, 10)
        expected_scene.addPixmap(black_ball).setPos(63, 10)
        expected_scene.addPixmap(black_ball).setPos(37, 36)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 B W . . 5

3 . . . . 3

1 . . . . 1
  A C E G
   B D F
 6 B . . 6

 4 . . . 4

 2 . . . 2
   B D F
"""))

        display.resize(QSize(300, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_resize_wide(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(400, 240, 'spline_resize_wide') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(51, 0)
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(white_ball).setPos(61, 10)
        expected_scene.addPixmap(black_ball).setPos(113, 10)
        expected_scene.addPixmap(black_ball).setPos(217, 62)
        expected_scene.addPixmap(white_ball).setPos(290, 88)
        add_text(expected_scene, 'to move', 320, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(QSize(400, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_resize_narrow(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(150, 240, 'spline_resize_narrow') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 150, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(120, 123))).setPos(0, 59)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(30, 30))

        expected_scene.addPixmap(black_ball).setPos(121, 103)
        add_text(expected_scene, f'to move', 136, 137, 5)
        expected_scene.render(expected)

        display = SplineDisplay()

        display.resize(QSize(150, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_hover_enter(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_hover_enter') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        new_piece = expected_scene.addPixmap(black_ball)
        new_piece.setPos(115, 114)
        new_piece.setOpacity(0.5)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(QSize(300, 240))
        display.on_hover_enter(piece_item)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_click(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_click') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(115, 114)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(QSize(300, 240))
        display.on_click(piece_item)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_hover_leave(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_hover_leave') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        expected_scene.addPixmap(black_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(QSize(300, 240))
        display.on_hover_enter(piece_item)
        display.on_hover_leave(piece_item)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_hover_enter_existing(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_hover_enter_existing') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(115, 114)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""))
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(QSize(300, 240))
        display.on_hover_enter(piece_item)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_hover_leave_existing(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_hover_leave_existing') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(115, 114)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""))
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(QSize(300, 240))
        display.on_hover_leave(piece_item)

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_double_update(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'spline_double_update') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 300, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(11, 10)
        expected_scene.addPixmap(white_ball).setPos(63, 10)
        expected_scene.addPixmap(black_ball).setPos(115, 62)
        expected_scene.addPixmap(white_ball).setPos(240, 88)
        add_text(expected_scene, 'to move', 270, 155, 11)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.resize(QSize(300, 240))
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 . . . W 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))
        display.update(display.game.create_board("""\
  A C E G
7 B W . . 7

5 . . B . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.scene.render(actual)
