from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QFont, QResizeEvent
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from shibumi.spline.game import SplineState
from zero_play.game_display import center_text_item
from zero_play.pixmap_differ import PixmapDiffer, render_display

from shibumi.spline.display import SplineDisplay


def trigger_resize(view: QGraphicsView, width: int, height: int):
    event = QResizeEvent(QSize(width, height), QSize(1, 1))
    view.resizeEvent(event)


def add_text(scene: QGraphicsScene, text: str, x: int, y: int, font_size: int):
    font = QFont(SplineDisplay.default_font)
    font.setPointSize(font_size)
    text_item = scene.addSimpleText(text, font)
    center_text_item(text_item, x, y)


# noinspection DuplicatedCode
def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)

        expected_scene.render(expected)

        display = SplineDisplay()

        display.resize(348, 264)

        render_display(display, actual)
    black_icon = SplineDisplay.load_pixmap('ball-b-shadow-1.png').toImage()
    assert display.ui.player_pixmap.pixmap().toImage() == black_icon
    assert display.ui.move_text.text() == 'to move'


# noinspection DuplicatedCode
def test_first_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
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
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update_board(SplineState("""\
  A C E G
7 W B . . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(348, 264)

        render_display(display, actual)
    white_icon = SplineDisplay.load_pixmap('ball-w-shadow-1.png').toImage()
    assert display.ui.player_pixmap.pixmap().toImage() == white_icon


# noinspection DuplicatedCode
def test_second_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
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
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update_board(SplineState("""\
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

        display.resize(348, 264)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_resize_wide(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((340, 240)) as (
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
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update_board(SplineState("""\
  A C E G
7 W B . . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(468, 264)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_resize_narrow(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((120, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 120, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(120, 123))).setPos(0, 59)

        expected_scene.render(expected)

        display = SplineDisplay()

        display.resize(204, 264)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_hover_enter(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        new_piece = expected_scene.addPixmap(black_ball)
        new_piece.setPos(115, 114)
        new_piece.setOpacity(0.5)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(348, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_click(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(115, 114)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(348, 264)
        display.grab()  # Force layout to recalculate.

        display.on_click(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_hover_leave(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        expected_scene.render(expected)

        display = SplineDisplay()
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(348, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)
        display.on_hover_leave(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_hover_leave_existing(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(240, 240))).setPos(1, 0)
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected_scene.addPixmap(black_ball).setPos(115, 114)
        expected_scene.render(expected)

        display = SplineDisplay()
        display.update_board(SplineState("""\
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

        display.resize(348, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_leave(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_double_update(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 240)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
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
        expected_scene.render(expected)

        display = SplineDisplay()
        trigger_resize(display, 300, 240)
        display.update_board(SplineState("""\
  A C E G
7 W B . . 7

5 . . . W 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))
        display.update_board(SplineState("""\
  A C E G
7 B W . . 7

5 . . B . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(348, 264)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_coordinates(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((240, 200)) as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 200)
        expected_scene.addPixmap(
            SplineDisplay.load_pixmap('board-1.png',
                                      QSize(160, 160))).setPos(36, 0)

        for i in range(7):
            add_text(expected_scene, str(7-i), 15+i % 2*10, i*17+27, 10)
            add_text(expected_scene, chr(65+i), i*17+64, 178-i % 2*10, 10)

        expected_scene.render(expected)

        display = SplineDisplay()
        display.resize(348, 224)

        display.show_coordinates = True

        render_display(display, actual)
