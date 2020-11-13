import pytest

from shibumi.sandbox.game import SandboxState
from shibumi.shibumi_game_state import MoveType


def test_move_black():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B B . 1
  A C E G
"""

    board2 = board.make_move(2)

    assert board2.display() == expected_board


def test_move_white():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B W . 1
  A C E G
"""

    board2 = board.make_move(32)

    assert board2.display() == expected_board


def test_move_red():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B R . 1
  A C E G
"""

    board2 = board.make_move(62)

    assert board2.display() == expected_board


def test_remove():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B W . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
"""

    move = board.get_index(height=0, row=0, column=2, move_type=MoveType.REMOVE)
    board2 = board.make_move(move)

    assert board2.display() == expected_board
    assert move == 92


def test_drop():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . B B . 3

1 . B B . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . W . 2
   B D F
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . B B . 3

1 . W B . 1
  A C E G
"""

    board2 = board.make_move(91)

    assert board2.display() == expected_board


def test_drop_double():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 B B B . 5

3 B B B . 3

1 B B B . 1
  A C E G
   B D F
 6 . . . 6

 4 W W . 4

 2 W W . 2
   B D F
    C E
  5 . . 5

  3 R . 3
    C E
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 B B B . 5

3 B B B . 3

1 B B W . 1
  A C E G
   B D F
 6 . . . 6

 4 W W . 4

 2 W R . 2
   B D F
"""

    board2 = board.make_move(92)

    assert board2.display() == expected_board


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 8, False, 'already occupied, black playing'),
                          (8, 16, True, 'unoccupied'),
                          (16, 18, False, 'already occupied, level 2'),
                          (18, 19, True, 'unoccupied and supported'),
                          (19, 30, False, 'unsupported'),
                          (30, 38, False, 'already occupied, white playing'),
                          (38, 46, True, 'unoccupied'),
                          (46, 48, False, 'already occupied, level 2'),
                          (48, 49, True, 'unoccupied and supported'),
                          (49, 60, False, 'unsupported'),
                          (60, 68, False, 'already occupied, red playing'),
                          (68, 76, True, 'unoccupied'),
                          (76, 78, False, 'already occupied, level 2'),
                          (78, 79, True, 'unoccupied and supported'),
                          (79, 90, False, 'unsupported'),
                          (90, 91, True, 'remove and drop'),
                          (91, 92, False, 'cannot remove pinned'),
                          (92, 93, True, 'remove and drop'),
                          (93, 94, True, 'remove existing'),
                          (94, 95, True, 'remove and drop'),
                          (95, 96, False, 'cannot remove pinned'),
                          (96, 97, True, 'remove and drop'),
                          (97, 98, True, 'remove existing'),
                          (98, 106, False, 'nothing to remove'),
                          (106, 108, True, 'remove level 2'),
                          (108, 120, False, 'nothing to remove')])
def test_is_valid(start: int, end: int, expected_valid: bool, reason: str):
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B B B B 3

1 W W W W 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 R R . 2
   B D F
""")

    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid


def test_display_move():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")

    assert board.display_move(2) == 'B1E'
    assert board.display_move(32) == 'W1E'
    assert board.display_move(62) == 'R1E'
    assert board.display_move(92) == 'x1E'
