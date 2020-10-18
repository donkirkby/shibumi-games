from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsScene, QApplication

from shibumi.sandbox.display import SandboxDisplay
from shibumi.sandbox.game import SandboxState
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
    display.selected_colour = SandboxState.WHITE
    
    assert display.ui.move_white.isChecked()


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
