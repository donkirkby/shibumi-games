from shibumi.spaiji.display import SpaijiDisplay


def test_start(application):
    display = SpaijiDisplay()

    assert display.ui.move_black.isVisibleTo(display)
    assert display.ui.move_white.isVisibleTo(display)


def test_second_move(application):
    display = SpaijiDisplay()
    display.ui.move_white.setChecked(True)

    display.make_move(32)  # White

    assert display.ui.move_black.isVisibleTo(display)
    assert not display.ui.move_white.isVisibleTo(display)
    assert display.ui.move_black.isChecked()
