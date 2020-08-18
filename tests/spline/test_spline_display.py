from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from zero_play.pixmap_differ import PixmapDiffer

from shibumi.spline.display import SplineDisplay


def test_empty(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'display_splinex') as (actual, expected):
        expected.drawPixmap(1, 0, SplineDisplay.load_pixmap('board-1.png',
                                                            QSize(240, 240)))

        display = SplineDisplay()

        display.resize(QSize(240, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_first_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240, 'spline_first_level') as (
            actual,
            expected):
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected.drawPixmap(1, 0, SplineDisplay.load_pixmap('board-1.png',
                                                            QSize(240, 240)))
        expected.drawPixmap(11, 10, white_ball)
        expected.drawPixmap(63, 10, black_ball)
        expected.drawPixmap(167, 62, white_ball)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 . . . W 5

3 . . . . 3

1 . . . . 1
  A C E G
"""))

        display.resize(QSize(240, 240))

        display.scene.render(actual)


# noinspection DuplicatedCode
def test_second_level(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(240, 240,
                                       'spline_second_level',
                                       max_diff=60) as (actual, expected):
        white_ball = SplineDisplay.load_pixmap('ball-w-shadow-1.png',
                                               QSize(60, 60))
        black_ball = SplineDisplay.load_pixmap('ball-b-shadow-1.png',
                                               QSize(60, 60))

        expected.drawPixmap(1, 0, SplineDisplay.load_pixmap('board-1.png',
                                                            QSize(240, 240)))
        expected.drawPixmap(11, 10, white_ball)
        expected.drawPixmap(63, 10, black_ball)
        expected.drawPixmap(11, 62, black_ball)
        expected.drawPixmap(63, 62, white_ball)
        expected.drawPixmap(37, 36, white_ball)

        display = SplineDisplay()
        display.update(display.game.create_board("""\
  A C E G
7 W B . . 7

5 B W . . 5

3 . . . . 3

1 . . . . 1
  A C E G
   B D F
 6 W . . 6

 4 . . . 4

 2 . . . 2
   B D F
"""))

        display.resize(QSize(240, 240))

        display.scene.render(actual)
