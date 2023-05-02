from shibumi.sparks.display import SparksDisplay


def test_start(application):
    display = SparksDisplay()

    assert display.ui.remove.isVisibleTo(display)
    assert not display.ui.move_white.isVisibleTo(display)
    assert not display.ui.move_black.isVisibleTo(display)
    assert not display.ui.move_red.isVisibleTo(display)


def test_second_move(application):
    display = SparksDisplay()

    display.make_move(1)

    assert not display.ui.remove.isVisibleTo(display)
    assert display.ui.move_white.isVisibleTo(display)
    assert not display.ui.move_black.isVisibleTo(display)
    assert not display.ui.move_red.isVisibleTo(display)
