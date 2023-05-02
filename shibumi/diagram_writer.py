from pathlib import Path
from textwrap import dedent

from PySide6.QtGui import QPainter, QColor

from shibumi.sandbox.game import SandboxState
from shibumi.shibumi_display import ShibumiDisplay
from shibumi.shibumi_game_state import ShibumiGameState
from shibumi.spaiji.display import SpaijiDisplay
from shibumi.spaiji.game import SpaijiState
from shibumi.spline.display import SplineDisplay
from shibumi.spline.game import SplineState
from shibumi.sploof.display import SploofDisplay
from shibumi.sploof.state import SploofState
from zero_play.diagram_writer import DiagramWriter
from zero_play.game_display import center_text_item


class ShibumiDiagramWriter(DiagramWriter):
    def __init__(self, state_text: str):
        state = SandboxState(state_text)
        display = ShibumiDisplay(state)
        display.resize(300, 224)
        display.ui.game_display.grab()  # Force layout.
        super().__init__(display)

    def add_text(self, text: str, row: int, column: int, level: int = 0):
        display = self.display
        assert isinstance(display, ShibumiDisplay)
        text_item = display.scene().addSimpleText(text)
        label = display.column_labels[6]
        piece_item = display.item_levels[level][row][column]
        font = label.font()
        font.setPixelSize(round(piece_item.pixmap().height() * 0.75))
        text_item.setFont(font)
        game_state = display.current_state
        assert isinstance(game_state, ShibumiGameState)
        if game_state.get_levels()[level][row][column] == game_state.BLACK:
            text_item.setBrush(QColor('white'))
        x = piece_item.x() + piece_item.pixmap().width() // 2
        y = piece_item.y() + round(piece_item.pixmap().height() * 0.45)
        center_text_item(text_item, x, y)


class SpaijiLossDiagram(DiagramWriter):
    def __init__(self):
        display = SpaijiDisplay()
        display.update_board(SpaijiState('''\
  A C E G
7 B W W W 7

5 B R R B 5

3 W R R B 3

1 B B W B 1
  A C E G
   B D F
 6 W W B 6

 4 B R W 4

 2 W B W 2
   B D F
    C E
  5 W B 5

  3 B B 3
    C E
     D
   4 W 4
     D
>B
'''))
        display.resize(300, 224)
        super().__init__(display)

    def draw(self, painter: QPainter):
        super().draw(painter)
        pen = painter.pen()
        pen.setColor(QColor('darkgrey'))
        painter.setPen(pen)
        w = self.width
        h = self.height
        size = int(w*0.06)
        x = int(w*0.49)
        y = int(h*0.47)
        painter.drawLine(x, y-size, x, y+size)
        painter.drawLine(x-size, y, x+size, y)
        x = int(w*0.6)
        y = int(h*0.37)
        painter.drawLine(x, y-size, x, y+size)
        painter.drawLine(x-size, y, x+size, y)


class SpaijiWinDiagram(SpaijiLossDiagram):
    def __init__(self):
        super().__init__()
        state = self.display.current_state
        assert isinstance(state, SpaijiState)
        board = state.board
        board[2, 1, 1] = state.WHITE
        board[3, 0, 0] = state.BLACK


class SparksStartDiagram(ShibumiDiagramWriter):
    def __init__(self):
        super().__init__(dedent('''\
              A C E G
            7 W B W B 7
            
            5 B W B W 5
            
            3 W B W B 3
            
            1 B W B W 1
              A C E G
            '''))


class SparksMove1aDiagram(ShibumiDiagramWriter):
    def __init__(self):
        super().__init__(dedent('''\
              A C E G
            7 W B W B 7
            
            5 B W B W 5
            
            3 W B W B 3
            
            1 B W B W 1
              A C E G
            '''))
        self.add_text('a', 1, 2)


class SparksMove1bDiagram(ShibumiDiagramWriter):
    def __init__(self):
        super().__init__(dedent('''\
              A C E G
            7 W B W B 7
            
            5 B W B W 5
            
            3 W B R B 3
            
            1 B W B W 1
              A C E G
               B D F
             6 W . .
            
             4 . . .
            
             2 . . .
               B D F
            '''))
        self.add_text('x', 1, 2)
        self.add_text('a', 2, 0, 1)


class SparksMove2aDiagram(SparksMove1bDiagram):
    def __init__(self):
        super().__init__()
        self.add_text('b', 2, 0)


class SparksMove2bDiagram(ShibumiDiagramWriter):
    def __init__(self):
        super().__init__(dedent('''\
              A C E G
            7 W B W B 7

            5 W W B W 5

            3 W B R B 3

            1 B W B W 1
              A C E G
               B D F
             6 . . R

             4 . . B

             2 . . .
               B D F
            '''))
        self.add_text('x', 1, 2)
        self.add_text('a', 2, 0)
        self.add_text('y', 2, 2, 1)
        self.add_text('b', 1, 2, 1)


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
        pen.setColor(QColor('darkgrey'))
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
        pen.setColor(QColor('darkgrey'))
        painter.setPen(pen)
        w = self.width
        h = self.height
        x = int(w*0.71)
        painter.drawLine(x, int(h * 0.48), x, int(h * 0.7))


def main():
    rules_path = Path(__file__).parent.parent / "docs" / "rules"
    SpaijiLossDiagram().write(rules_path / "spaiji_loss.png")
    SpaijiWinDiagram().write(rules_path / "spaiji_win.png")
    SparksStartDiagram().write(rules_path / "sparks_start.png")
    SparksMove1aDiagram().write(rules_path / "sparks_move1a.png")
    SparksMove1bDiagram().write(rules_path / "sparks_move1b.png")
    SparksMove2aDiagram().write(rules_path / "sparks_move2a.png")
    SparksMove2bDiagram().write(rules_path / "sparks_move2b.png")
    SplineDiagram().write(rules_path / "spline.png")
    SplineDiagram2().write(rules_path / "spline2.png")
    SploofStartDiagram().write(rules_path / "sploof_start.png")
    SploofWinDiagram().write(rules_path / "sploof_win.png")
    SploofRowDiagram().write(rules_path / "sploof_row.png")
    SploofBlockedDiagram().write(rules_path / "sploof_blocked.png")


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    SparksMove2bDiagram().demo()
