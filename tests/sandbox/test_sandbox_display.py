from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsScene, QApplication

from shibumi.sandbox.display import SandboxDisplay
from shibumi.sandbox.game import SandboxState
from shibumi.shibumi_game_state import MoveType
from zero_play.pixmap_differ import PixmapDiffer, render_display


# noinspection DuplicatedCode
def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'sandbox_empty') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)

        expected_scene.render(expected)

        display = SandboxDisplay()

        display.resize(336, 264)

        render_display(display, actual)
    assert not display.ui.move_black.icon().isNull()
    assert not display.ui.move_white.icon().isNull()
    assert display.ui.move_black.isChecked()


# noinspection DuplicatedCode
def test_selected_colour(pixmap_differ: PixmapDiffer):
    display = SandboxDisplay()

    display.resize(336, 264)
    display.selected_move_type = MoveType.WHITE
    
    assert display.ui.move_white.isChecked()


def test_make_move_white(application: QApplication):
    expected_text = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . W . 1
  A C E G
"""
    display = SandboxDisplay()
    display.selected_move_type = MoveType.WHITE

    piece_item = display.item_levels[0][0][2]
    display.on_click(piece_item)

    assert display.current_state.display() == expected_text


def test_make_move_red(application: QApplication):
    expected_text = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . R . 1
  A C E G
"""
    display = SandboxDisplay()
    display.selected_move_type = MoveType.RED

    piece_item = display.item_levels[0][0][2]
    display.on_click(piece_item)

    assert display.current_state.display() == expected_text


# noinspection DuplicatedCode
def test_red(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'sandbox_red') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        white_ball = SandboxDisplay.load_pixmap('ball-w-shadow-1.png',
                                                QSize(60, 60))
        black_ball = SandboxDisplay.load_pixmap('ball-b-shadow-1.png',
                                                QSize(60, 60))
        red_ball = SandboxDisplay.load_pixmap('ball-r-shadow-1.png',
                                              QSize(60, 60))

        expected_scene.addPixmap(white_ball).setPos(11, 10)
        expected_scene.addPixmap(red_ball).setPos(63, 10)
        expected_scene.addPixmap(black_ball).setPos(167, 62)
        expected_scene.render(expected)

        display = SandboxDisplay()
        display.update_board(SandboxState("""\
  A C E G
7 W R . . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(336, 264)

        render_display(display, actual)
    assert display.ui.player_pixmap.pixmap() is None


# noinspection DuplicatedCode
def test_hover_enter_red(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'sandbox_hover_enter_red') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        red_ball = SandboxDisplay.load_pixmap('ball-r-shadow-1.png',
                                              QSize(60, 60))

        new_piece = expected_scene.addPixmap(red_ball)
        new_piece.setPos(115, 114)
        new_piece.setOpacity(0.5)
        expected_scene.render(expected)

        display = SandboxDisplay()
        display.selected_move_type = MoveType.RED
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(336, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_hover_enter_remove(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240,
                                       'sandbox_hover_enter_remove') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        white_ball = SandboxDisplay.load_pixmap('ball-w-shadow-1.png',
                                                QSize(60, 60))

        new_piece = expected_scene.addPixmap(white_ball)
        new_piece.setPos(115, 114)
        new_piece.setOpacity(0.5)
        expected_scene.render(expected)

        display = SandboxDisplay()
        display.update_board(SandboxState('''\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . W . 3

1 . . . . 1
  A C E G
'''))
        display.selected_move_type = MoveType.REMOVE
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(336, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)

        render_display(display, actual)


# noinspection DuplicatedCode
def test_hover_enter_leave(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240,
                                       'sandbox_hover_enter_leave') as (
            actual,
            expected):
        expected_scene = QGraphicsScene(0, 0, 240, 240)
        expected_scene.addPixmap(
            SandboxDisplay.load_pixmap('board-1.png',
                                       QSize(240, 240))).setPos(1, 0)
        white_ball = SandboxDisplay.load_pixmap('ball-w-shadow-1.png',
                                                QSize(60, 60))

        new_piece = expected_scene.addPixmap(white_ball)
        new_piece.setPos(115, 114)
        expected_scene.render(expected)

        display = SandboxDisplay()
        display.update_board(SandboxState('''\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . W . 3

1 . . . . 1
  A C E G
'''))
        display.selected_move_type = MoveType.REMOVE
        height = 0
        row = 1
        column = 2
        piece_item = display.item_levels[height][row][column]

        display.resize(336, 264)
        display.grab()  # Force layout to recalculate.

        display.on_hover_enter(piece_item)
        display.on_hover_leave(piece_item)

        render_display(display, actual)
