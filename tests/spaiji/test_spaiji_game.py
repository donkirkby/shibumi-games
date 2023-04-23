import pytest

from shibumi.spaiji.game import SpaijiState


def test_start():
    board = SpaijiState()
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
>W
"""

    assert board.display() == expected_board


def test_first_move():
    board = SpaijiState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . B . 1
  A C E G
>W(1E)
"""
    board2 = board.make_move(2)

    assert board2.display() == expected_board


def test_move2():
    board = SpaijiState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . B . 1
  A C E G
>W(1E)
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . W B . 1
  A C E G
>B
"""
    board2 = board.make_move(31)

    assert board2.display() == expected_board


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 8, False, 'already occupied, playing black'),
                          (8, 16, True, 'unoccupied'),
                          (16, 19, True, 'unoccupied and supported'),
                          (19, 30, False, 'unsupported'),
                          (30, 38, False, 'already occupied, playing white'),
                          (38, 46, True, 'unoccupied'),
                          (46, 49, True, 'unoccupied and supported'),
                          (49, 60, False, 'unsupported')])
def test_valid_first_moves(start: int,
                           end: int,
                           expected_valid: bool,
                           reason: str):
    board = SpaijiState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B W B W 3

1 B W B W 1
  A C E G
>W
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 9, False, 'already occupied, playing black'),
                          (9, 10, True, 'unoccupied, same height neighbour'),
                          (10, 16, False, 'not neighbouring first move'),
                          (16, 18, True, 'supported neighbours'),
                          (18, 19, False, 'not neighbouring first move'),
                          (19, 30, False, 'unsupported'),
                          (30, 60, False, 'already played white')])
def test_valid_second_moves(start: int,
                            end: int,
                            expected_valid: bool,
                            reason: str):
    board = SpaijiState("""\
  A C E G
7 . . . . 7

5 W . . . 5

3 B W B W 3

1 B W B W 1
  A C E G
>W(3C)
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid


def test_is_win():
    board = SpaijiState("""\
  A C E G
7 B B B B 7

5 W W W W 5

3 W W W W 3

1 B B B B 1
  A C E G
   B D F
 6 B B W 6

 4 W W W 4

 2 B B B 2
   B D F
    C E
  5 B W 5

  3 W B 3
    C E
     D
   4 W 4
     D
>B
""")

    assert board.is_win(board.WHITE)
    assert not board.is_win(board.BLACK)


def test_get_index():
    board = SpaijiState()

    black_move = board.get_index(0, 0, 2, board.BLACK)
    white_move = board.get_index(0, 0, 2, board.WHITE)

    assert black_move == 2
    assert white_move == 32


def test_display_move():
    board = SpaijiState()

    black_move = board.display_move(2)
    white_move = board.display_move(32)

    assert black_move == 'B1E'
    assert white_move == 'W1E'


def test_active_player():
    board1 = SpaijiState('''\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . W B 1
  A C E G
>B
''')
    board2 = board1.make_move(15)

    assert board2.get_active_player() == board1.BLACK


def test_piece_count():
    board = SpaijiState('''\
  A C E G
7 . . . . 7

5 . . . W 5

3 . . . B 3

1 . . W B 1
  A C E G
>W
''')

    black_count = board.get_piece_count(board.BLACK)
    white_count = board.get_piece_count(board.WHITE)

    assert black_count == 2
    assert white_count == 1


def test_count_group():
    board = SpaijiState('''\
  A C E G
7 . . . . 7

5 . . . B 5

3 . W W W 3

1 . . B B 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . . W 2
   B D F
>B(3C)
''')

    white_count = board.get_piece_count(board.WHITE)

    assert white_count == 4


def test_group_with_covered_pieces():
    board = SpaijiState('''\
  A C E G
7 W W B W 7

5 B B W B 5

3 B W B W 3

1 W B B W 1
  A C E G
   B D F
 6 W W B 6

 4 B B W 4

 2 B W B 2
   B D F
    C E
  5 B W 5

  3 W W 3
    C E
>W(5E)
''')

    black_count = board.get_piece_count(board.BLACK)

    assert black_count == 9


def test_move_count_ignores_state():
    board = SpaijiState('''\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . B 3

1 . . W B 1
  A C E G
>B(3G)
''')

    black_count = board.get_move_count()

    assert black_count == 3


def test_first_move_no_neighbours():
    """ Can't pick a first move with no neighbours. """
    board = SpaijiState('''\
  A C E G
7 . . . . 7

5 . . . . 5

3 W W . . 3

1 B B . . 1
  A C E G
>W
''')

    valid_moves = board.get_valid_moves()

    assert not valid_moves[16]


def test_early_end():
    """ End game when there are no valid moves. """
    board = SpaijiState('''\
  A C E G
7 B W B W 7

5 W B W B 5

3 B W B W 3

1 W B W B 1
  A C E G
   B D F
 6 . W . 6

 4 B . B 4

 2 . W . 2
   B D F
>W
''')

    assert board.get_piece_count(board.WHITE) == 3
    assert board.get_piece_count(board.BLACK) == 3
    assert board.is_ended()
    # Tie goes to black
    assert not board.is_win(board.WHITE)
    assert board.is_win(board.BLACK)
