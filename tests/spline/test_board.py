# noinspection PyPackageRequirements
import pytest

from shibumi.spline.board import Board, Player


def test_start_display():
    board = Board()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""

    display = str(board)

    assert expected_display == display


def test_spaces_count():
    board = Board()

    spaces_count = board.get_spaces_count()

    assert 30 == spaces_count


def test_start_valid_moves():
    board = Board()
    expected_moves = [True] * 16 + [False] * 14

    valid_moves = board.get_valid_moves()

    assert expected_moves == valid_moves.tolist()


def test_add_stone_display():
    board = Board()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""

    board.add_stone('3', 'E', Player.BLACK)
    display = str(board)

    assert expected_display == display


def test_init_text():
    expected_display = """\
  A C E G
7 . . . . 7

5 . W . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""
    board = Board(text=expected_display)

    display = str(board)

    assert expected_display == display


def test_init_pieces():
    expected_display = """\
  A C E G
7 . . . . 7

5 . W . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""
    board1 = Board(text=expected_display)
    board2 = Board()
    board3 = board2.with_np_pieces(board1.pieces)

    display = str(board3)

    assert expected_display == display


def test_init_text_second_level():
    expected_display = """\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
   B D F
 6 . . . 6

 4 . R . 4

 2 . . . 2
   B D F
"""
    board = Board(text=expected_display)

    display = str(board)

    assert expected_display == display


def test_init_text_partial():
    text = """\
Headers ignored
! WxB
garbage
??B W
"""
    expected_display = """\
  A C E G
7 W B . . 7

5 B W . . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""
    board = Board(text=text)

    display = str(board)

    assert expected_display == display


def test_init_text_bad():
    text = """\
  A C E G
7 . . . . 7

5 . W . . 5

3 . . B . 3

1 . X . . 1
  A C E G
"""
    with pytest.raises(ValueError, match="Unexpected 'X' at line 8, column 5."):
        Board(text=text)


def test_add_stone_second_level():
    board = Board(text="""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")
    expected_display = """\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
   B D F
 6 . . . 6

 4 . R . 4

 2 . . . 2
   B D F
"""

    board.add_stone('4', 'D', Player.RED)
    display = str(board)

    assert expected_display == display


def test_add_stone_third_level():
    board = Board(text="""\
  A C E G
7 . W B W 7

5 . W B W 5

3 . W B B 3

1 . . . . 1
  A C E G
   B D F
 6 . W B 6

 4 . R W 4

 2 . . . 2
   B D F
""")
    expected_display = """\
  A C E G
7 . W B W 7

5 . W B W 5

3 . W B B 3

1 . . . . 1
  A C E G
   B D F
 6 . W B 6

 4 . R W 4

 2 . . . 2
   B D F
    C E
  5 . B 5

  3 . . 3
    C E
"""

    board.add_stone('5', 'E', Player.BLACK)
    display = str(board)

    assert expected_display == display


def test_add_stone_bad_row():
    board = Board(text="""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 5C.'):
        board.add_stone('5', 'C', Player.RED)


def test_full_spaces_valid_moves():
    board = Board(text="""\
  A C E G
7 . . . . 7

5 . W . . 5

3 . . B . 3

1 . . . . 1
  A C E G
""")
    expected_valid_moves = [True] * 16 + [False] * 14
    # full spaces are no longer valid moves
    expected_valid_moves[6] = expected_valid_moves[9] = False

    valid_moves = board.get_valid_moves()

    assert expected_valid_moves == valid_moves.tolist()


def test_second_level_valid_moves():
    board = Board(text="""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")
    expected_valid_moves = [True] * 16 + [False] * 14
    # full spaces are no longer valid moves
    expected_valid_moves[5:7] = expected_valid_moves[9:11] = [False, False]
    # centre of second level is now supported
    expected_valid_moves[20] = True

    valid_moves = board.get_valid_moves()

    assert expected_valid_moves == valid_moves.tolist()


def test_win_row():
    board = Board(text="""\
  A C E G
7 . . . . 7

5 W W W W 5

3 . B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = Player.WHITE

    winner = board.get_winner()

    assert expected_winner == winner


def test_win_column():
    board = Board(text="""\
  A C E G
7 W W B . 7

5 W W B W 5

3 W B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = Player.BLACK

    winner = board.get_winner()

    assert expected_winner == winner


def test_win_column_level_2():
    board = Board(text="""\
  A C E G
7 W W W . 7

5 W W B W 5

3 W B B . 3

1 . B B . 1
  A C E G
   B D F
 6 B W . 6

 4 B W B 4

 2 . W . 2
   B D F
""")
    expected_winner = Player.WHITE

    winner = board.get_winner()

    assert expected_winner == winner


def test_win_diagonal():
    board = Board(text="""\
  A C E G
7 W W B . 7

5 W W B B 5

3 W B W B 3

1 . B B W 1
  A C E G
""")
    expected_winner = Player.WHITE

    winner = board.get_winner()

    assert expected_winner == winner
