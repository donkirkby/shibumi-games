from pathlib import Path

from PySide2.QtGui import QPainter

from shibumi.spline.display import SplineDisplay
from shibumi.spline.game import SplineState
from shibumi.sploof.display import SploofDisplay
from shibumi.sploof.state import SploofState
from zero_play.diagram_writer import DiagramWriter


class SplineDiagram(DiagramWriter):
    def __init__(self):
        display = SplineDisplay()
        display.update_board(SplineState('''\
  A C E G
7 W B W . 7

5 B B B W 5

3 W B B . 3

1 W W B . 1
  A C E G
   B D F
 6 W B . 6

 4 W . . 4

 2 W . . 2
   B D F
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        w = self.width
        h = self.height
        x = int(w*0.28)
        painter.drawLine(x, int(h*0.26), x, int(h*0.7))


class SplineDiagram2(DiagramWriter):
    def __init__(self):
        display = SplineDisplay()
        display.update_board(SplineState('''\
  A C E G
7 W B W B 7

5 B W B W 5

3 W B W B 3

1 W W B . 1
  A C E G
   B D F
 6 W B B 6

 4 B B W 4

 2 W W . 2
   B D F
    C E
  5 . B 5

  3 B . 3
    C E
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        pen = painter.pen()
        pen.setColor('darkgrey')
        painter.setPen(pen)
        w = self.width
        h = self.height
        length = int(w*0.2)
        x = int(w*0.4)
        y = int(h*0.58)
        painter.drawLine(x, y, x+length, y-length)


class SploofStartDiagram(DiagramWriter):
    def __init__(self):
        display = SploofDisplay()
        display.update_board(SploofState())
        display.resize(300, 224)
        super().__init__(display)


class SploofWinDiagram(DiagramWriter):
    def __init__(self):
        display = SploofDisplay()
        display.update_board(SploofState('''\
  A C E G
7 B B W W 7

5 R W W W 5

3 W B W R 3

1 B B R W 1
  A C E G
   B D F
 6 B . . 6

 4 B W W 4

 2 W B B 2
   B D F
    C E
  5 . . 5

  3 W . 3
    C E
>W(1,2)
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        w = self.width
        h = self.height
        length = int(self.width*0.32)
        x = int(w*0.28)
        y = int(h*0.7)
        painter.drawLine(x, y, x+length, y-length)


class SploofRowDiagram(DiagramWriter):
    def __init__(self):
        display = SploofDisplay()
        display.update_board(SploofState('''\
  A C E G
7 R R R R 7

5 R B B R 5

3 W W W W 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . B 4

 2 . . . 2
   B D F
>W(1,2)
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        w = self.width
        h = self.height
        y = int(h*0.59)
        painter.drawLine(int(w*0.18), y, int(w*0.81), y)


class SploofBlockedDiagram(DiagramWriter):
    def __init__(self):
        display = SploofDisplay()
        display.update_board(SploofState('''\
  A C E G
7 . R R R 7

5 . B B R 5

3 W W W W 3

1 R R R R 1
  A C E G
   B D F
 6 . B . 6

 4 . . W 4

 2 . . B 2
   B D F
>W(1,2)
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        pen = painter.pen()
        pen.setColor('darkgrey')
        painter.setPen(pen)
        w = self.width
        h = self.height
        x = int(w*0.71)
        painter.drawLine(x, int(h * 0.48), x, int(h * 0.7))


def main():
    rules_path = Path(__file__).parent.parent / "docs" / "rules"
    SplineDiagram().write(rules_path / "spline.png")
    SplineDiagram2().write(rules_path / "spline2.png")
    SploofStartDiagram().write(rules_path / "sploof_start.png")
    SploofWinDiagram().write(rules_path / "sploof_win.png")
    SploofRowDiagram().write(rules_path / "sploof_row.png")
    SploofBlockedDiagram().write(rules_path / "sploof_blocked.png")


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    SplineDiagram2().demo()
