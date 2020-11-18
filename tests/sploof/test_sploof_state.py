import pytest

from shibumi.sploof.state import SploofState


def test_start():
    expected_display = """\
  A C E G
7 R R R R 7

5 R . . R 5

3 R . . R 3

1 R R R R 1
  A C E G
>W(2,2)
"""
    # Shows size of player's stock, followed by opponent's stock.
    state = SploofState()

    display = state.display()
    active_player = state.get_active_player()

    assert display == expected_display
    assert active_player == state.WHITE


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 8, False, 'occupied, playing white'),
                          (8, 12, True, 'empty'),
                          (12, 18, False, 'occupied'),
                          (18, 19, True, 'supported'),
                          (19, 30, False, 'unsupported'),
                          (30, 31, True, 'unpinned, removing red'),
                          (31, 32, False, 'pinned'),
                          (32, 35, True, 'unpinned'),
                          (35, 37, False, 'not red'),
                          (37, 38, True, 'unpinned'),
                          (38, 42, False, 'empty'),
                          (42, 46, True, 'unpinned'),
                          (46, 48, False, 'not red'),
                          (48, 60, False, 'empty')])
def test_valid_moves(start: int, end: int, expected_valid: bool, reason: str):
    board = SploofState("""\
  A C E G
7 R R R R 7

5 . . . . 5

3 R W B R 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 W B . 2
   B D F
>W(2,2)
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


def test_add_move():
    state1 = SploofState("""\
  A C E G
7 R R R R 7

5 . . . . 5

3 R W B R 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 W B . 2
   B D F
>W(2,2)
""")
    expected_display = """\
  A C E G
7 R R R R 7

5 W . . . 5

3 R W B R 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 W B . 2
   B D F
>B(2,1)
"""
    state2 = state1.make_move(8)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test_remove():
    state1 = SploofState("""\
  A C E G
7 R R R R 7

5 . . . . 5

3 R W B R 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 W B . 2
   B D F
>W(2,2)
""")
    expected_display = """\
  A C E G
7 R R R R 7

5 . . . . 5

3 R W B R 3

1 W R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . B . 2
   B D F
>B(2,4)
"""
    state2 = state1.make_move(30)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK
