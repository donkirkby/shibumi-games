import pytest

from shibumi.spire.state import SpireState


def test_start():
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
>B,R
"""
    state = SpireState()

    display = state.display()
    active_player = state.get_active_player()

    assert display == expected_display
    assert active_player == state.BLACK


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 8, False, 'already occupied, playing black'),
                          (8, 10, False, 'two neighbours match colour'),
                          (10, 12, True, 'only one matching neighbour'),
                          (12, 16, True, 'no neighbours'),
                          (16, 17, False, 'two supports match colour'),
                          (17, 19, True, 'only one matching support'),
                          (19, 30, False, 'no support'),
                          (30, 38, False, 'already occupied, playing red'),
                          (38, 46, True, 'unoccupied, fewer than two matches'),
                          (46, 47, True, 'supported, no matches'),
                          (47, 49, False, 'supported, two matches'),
                          (49, 60, False, 'unsupported')])
def test_lower_rows(start: int, end: int, expected_valid: bool, reason: str):
    board = SpireState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B B R B 3

1 W W R W 1
  A C E G
>B,R
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert (move, valid_moves[move]) == (move, expected_valid)


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 4, True, 'no neighbours, playing black'),
                          (4, 6, False, 'two neighbours match colour'),
                          (6, 8, True, 'only one matching neighbour'),
                          (8, 16, False, 'already occupied')])
def test_upper_rows(start: int, end: int, expected_valid: bool, reason: str):
    board = SpireState("""\
  A C E G
7 W W R W 7

5 B B R B 5

3 . . . . 3

1 . . . . 1
  A C E G
>B,R
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 19, False, 'already occupied, playing black'),
                          (19, 21, False, 'two neighbours match colour'),
                          (21, 22, True, 'only one matching neighbour'),
                          (22, 25, True, 'no neighbours'),
                          (25, 30, False, 'no support')])
def test_higher_level(start: int, end: int, expected_valid: bool, reason: str):
    board = SpireState("""\
  A C E G
7 B W B R 7

5 W R R W 5

3 B W B R 3

1 W R R W 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 B B R 2
   B D F
>B,R
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(30, 60, False, 'red already played this turn')])
def test_no_red(start: int, end: int, expected_valid: bool, reason: str):
    board = SpireState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B B R B 3

1 W W R W 1
  A C E G
>B
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


def test_winner():
    text = """\
  A C E G
7 B W B W 7

5 W B W B 5

3 B W B W 3

1 W B W B 1
  A C E G
   B D F
 6 . . . 6

 4 . R . 4

 2 . . . 2
   B D F
>B
"""
    state = SpireState(text)

    assert state.is_ended()
    assert state.get_winner() == state.WHITE
    assert state.is_win(state.WHITE)
    assert not state.is_win(state.BLACK)


def test_move_black():
    expected_display2 = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 B . . . 1
  A C E G
>W,R
"""
    state1 = SpireState()

    state2 = state1.make_move(0)
    display2 = state2.display()

    assert display2 == expected_display2


def test_move_red():
    expected_display2 = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 R . . . 1
  A C E G
>B
"""
    state1 = SpireState()

    state2 = state1.make_move(30)
    display2 = state2.display()

    assert display2 == expected_display2


def test_valid_colours():
    state = SpireState()
    expected_colours = (state.BLACK, state.RED)

    colours = state.get_valid_colours()

    assert colours == expected_colours


def test_valid_colours_no_red():
    state = SpireState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 R . . . 1
  A C E G
>B
""")
    expected_colours = (state.BLACK, )

    colours = state.get_valid_colours()

    assert colours == expected_colours


def test_get_index():
    state = SpireState()

    black_move = state.get_index(height=0,
                                 row=0,
                                 column=0,
                                 move_type=state.BLACK)
    red_move = state.get_index(height=0,
                               row=0,
                               column=0,
                               move_type=state.RED)
    white_move = state.get_index(height=0,
                                 row=0,
                                 column=0,
                                 move_type=state.WHITE)

    assert black_move == 0
    assert red_move == 30
    assert white_move == 0


def test_get_coordinates():
    state = SpireState()

    height, row, column = state.get_coordinates(31)

    assert height == 0
    assert row == 0
    assert column == 1


def test_display_move():
    state1 = SpireState()

    move1_display = state1.display_move(2)
    move2_display = state1.display_move(32)

    state2 = state1.make_move(1)
    move3_display = state2.display_move(2)

    assert move1_display == 'B1E'
    assert move2_display == 'R1E'
    assert move3_display == 'W1E'
