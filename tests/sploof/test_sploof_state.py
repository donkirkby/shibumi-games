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


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 9, False, 'occupied, playing white'),
                          (9, 11, False, 'empty stock'),
                          (11, 14, False, 'occupied'),
                          (14, 19, False, 'empty stock'),
                          (19, 30, False, 'unsupported'),
                          (30, 35, True, 'free, removing red'),
                          (35, 37, False, 'not red'),
                          (37, 39, True, 'free'),
                          (39, 41, False, 'empty'),
                          (41, 44, True, 'free'),
                          (44, 60, False, 'empty')])
def test_empty_stock(start: int, end: int, expected_valid: bool, reason: str):
    board = SploofState("""\
  A C E G
7 R R . . 7

5 R . . R 5

3 R W W R 3

1 R R R R 1
  A C E G
>W(0,6)
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


def test_get_index():
    state = SploofState("""\
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

    move = state.get_index(height=0, row=0, column=0, move_type=state.RED)

    assert move == 30


def test_display_move():
    state = SploofState()

    move_display = state.display_move(30)

    assert move_display == 'R1A'


def test_piece_count():
    state = SploofState("""\
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
>W(4,3)
""")

    assert state.get_piece_count(state.WHITE) == 4
    assert state.get_piece_count(state.BLACK) == 3


def test_no_valid_moves():
    state = SploofState("""\
  A C E G
7 W . W . 7

5 . W B W 5

3 W B W . 3

1 . W . W 1
  A C E G
>W(0,18)
""")

    assert state.get_winner() == state.BLACK


def test_base_row():
    state = SploofState("""\
  A C E G
7 R R R R 7

5 R B B R 5

3 W W W W 3

1 R R R R 1
  A C E G
   B D F
 6 . B . 6

 4 . . . 4

 2 . . . 2
   B D F
>B(1,0)
""")

    assert state.get_winner() == state.WHITE


def test_base_column():
    state = SploofState("""\
  A C E G
7 R R W R 7

5 R B W R 5

3 R B W R 3

1 R R W R 1
  A C E G
   B D F
 6 . . . 6

 4 B . . 4

 2 . . . 2
   B D F
>B(1,0)
""")

    assert state.get_winner() == state.WHITE


def test_cutoff_row():
    state = SploofState("""\
  A C E G
7 R R R R 7

5 R . B R 5

3 W W W W 3

1 R R R R 1
  A C E G
   B D F
 6 . . . 6

 4 . . B 4

 2 . . B 2
   B D F
>B(1,0)
""")

    assert state.get_winner() == state.NO_PLAYER


def test_cutoff_column():
    state = SploofState("""\
  A C E G
7 R R W R 7

5 R . W R 5

3 R B W R 3

1 R R W R 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . B B 2
   B D F
>B(1,0)
""")

    assert state.get_winner() == state.NO_PLAYER


def test_diagonal_win():
    state = SploofState("""\
  A C E G
7 R R R . 7

5 R B B R 5

3 R B W R 3

1 R R R W 1
  A C E G
   B D F
 6 . . . 6

 4 . W . 4

 2 . . W 2
   B D F
>B(1,0)
""")

    assert state.get_winner() == state.WHITE


def test_let_opponent_win():
    state1 = SploofState("""\
  A C E G
7 . . W W 7

5 . . W W 5

3 . . W W 3

1 B . R B 1
  A C E G
   B D F
 6 . . W 6

 4 . . . 4

 2 . . W 2
   B D F
>B(16,0)
""")

    state2 = state1.make_move(32)

    assert state2.get_winner() == state2.WHITE
