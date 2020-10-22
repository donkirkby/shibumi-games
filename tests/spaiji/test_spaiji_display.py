from shibumi.spaiji.display import SpaijiDisplay
from zero_play.pixmap_differ import PixmapDiffer


def test_start(pixmap_differ: PixmapDiffer):
    display = SpaijiDisplay()

    assert display.ui.move_black.isVisibleTo(display)
    assert display.ui.move_white.isVisibleTo(display)


def test_second_move(pixmap_differ: PixmapDiffer):
    display = SpaijiDisplay()
    display.ui.move_white.setChecked(True)

    display.make_move(32)  # White

    assert display.ui.move_black.isVisibleTo(display)
    assert not display.ui.move_white.isVisibleTo(display)
    assert display.ui.move_black.isChecked()
