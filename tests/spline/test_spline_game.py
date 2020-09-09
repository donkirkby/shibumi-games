# noinspection PyPackageRequirements
import pytest

from shibumi.spline.game import SplineGame


def test_start_display():
    game = SplineGame()
    board = game.create_board()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""

    display = game.display(board, show_coordinates=True)

    assert expected_display == display


def test_start_valid_moves():
    game = SplineGame()
    board = game.create_board()
    expected_moves = [True] * 16 + [False] * 14

    valid_moves = game.get_valid_moves(board)

    assert expected_moves == valid_moves.tolist()


def test_add_stone_display():
    game = SplineGame()
    board1 = game.create_board()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""

    move = game.parse_move('3E', board1)
    board2 = game.make_move(board1, move)
    display = game.display(board2, show_coordinates=True)

    assert expected_display == display


def test_add_stone_lower_case():
    game = SplineGame()
    board1 = game.create_board()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""

    move = game.parse_move('3e', board1)
    board2 = game.make_move(board1, move)
    display = game.display(board2, show_coordinates=True)

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
    game = SplineGame()
    board = game.create_board(text=expected_display)

    display = game.display(board, show_coordinates=True)

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
    game = SplineGame()
    board = game.create_board(text=expected_display)

    display = game.display(board, show_coordinates=True)

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
    game = SplineGame()
    board = game.create_board(text=text)

    display = game.display(board, show_coordinates=True)

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
    game = SplineGame()
    with pytest.raises(ValueError, match="Unexpected 'X' at line 8, column 5."):
        game.create_board(text=text)


def test_add_stone_second_level():
    game = SplineGame()
    board1 = game.create_board("""\
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

 4 . B . 4

 2 . . . 2
   B D F
"""

    move = game.parse_move('4D', board1)
    board2 = game.make_move(board1, move)
    display = game.display(board2, show_coordinates=True)

    assert expected_display == display


def test_add_stone_third_level():
    game = SplineGame()
    board1 = game.create_board("""\
  A C E G
7 . B B W 7

5 . W B W 5

3 . W B B 3

1 . . . . 1
  A C E G
   B D F
 6 . W B 6

 4 . B W 4

 2 . . . 2
   B D F
""")
    expected_display = """\
  A C E G
7 . B B W 7

5 . W B W 5

3 . W B B 3

1 . . . . 1
  A C E G
   B D F
 6 . W B 6

 4 . B W 4

 2 . . . 2
   B D F
    C E
  5 . W 5

  3 . . 3
    C E
"""

    move = game.parse_move('5e', board1)
    board2 = game.make_move(board1, move)
    display = game.display(board2, show_coordinates=True)

    assert expected_display == display


def test_add_stone_occupied_row():
    game = SplineGame()
    board1 = game.create_board("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 5C.'):
        game.parse_move('5C', board1)


def test_add_stone_bad_column():
    game = SplineGame()
    board1 = game.create_board("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 5X.'):
        game.parse_move('5X', board1)


def test_add_stone_bad_row():
    game = SplineGame()
    board1 = game.create_board("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 9C.'):
        game.parse_move('9C', board1)


def test_full_spaces_valid_moves():
    game = SplineGame()
    board = game.create_board("""\
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

    valid_moves = game.get_valid_moves(board)

    assert expected_valid_moves == valid_moves.tolist()


def test_second_level_valid_moves():
    game = SplineGame()
    board = game.create_board("""\
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

    valid_moves = game.get_valid_moves(board)

    assert expected_valid_moves == valid_moves.tolist()


def test_win_row():
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 . . . . 7

5 W W W W 5

3 . B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = game.WHITE

    winner = game.get_winner(board)

    assert expected_winner == winner


def test_win_column():
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 W W B . 7

5 W W B W 5

3 W B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = game.BLACK

    winner = game.get_winner(board)

    assert expected_winner == winner


def test_win_column_level_2():
    game = SplineGame()
    board = game.create_board("""\
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
    expected_winner = game.WHITE

    winner = game.get_winner(board)

    assert expected_winner == winner


def test_win_diagonal():
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 W W B . 7

5 W W B B 5

3 W B W B 3

1 . B B W 1
  A C E G
""")
    expected_winner = game.WHITE

    winner = game.get_winner(board)

    assert expected_winner == winner


def test_valid_moves_after_win():
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 . W B . 7

5 . W B . 5

3 . W B . 3

1 . . B . 1
  A C E G
""")
    expected_valid_moves = [False] * 30

    valid_moves = game.get_valid_moves(board)

    assert valid_moves.tolist() == expected_valid_moves


def test_get_levels():
    game = SplineGame()
    board = game.create_board("""\
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
    w = game.WHITE
    b = game.BLACK
    n = game.NO_PLAYER
    u = game.UNUSABLE
    expected_levels = [[[n, b, b, n],
                        [w, b, b, n],
                        [w, w, b, w],
                        [w, w, w, n]],
                       [[n, w, n, u],
                        [b, w, b, u],
                        [b, w, n, u],
                        [u, u, u, u]],
                       [[n, n, u, u],
                        [n, n, u, u],
                        [u, u, u, u],
                        [u, u, u, u]],
                       [[n, u, u, u],
                        [u, u, u, u],
                        [u, u, u, u],
                        [u, u, u, u]]]
    assert game.get_levels(board).tolist() == expected_levels


@pytest.mark.parametrize(['move_index', 'expected_display'],
                         [(0, '1A'),
                          (3, '1G'),
                          (4, '3A'),
                          (16, '2B')])
def test_display_move(move_index: int, expected_display: str):
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . . . 2
   B D F
""")

    display = game.display_move(board, move_index)

    assert display == expected_display


def test_get_move_count():
    game = SplineGame()
    board = game.create_board("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . B W . 3

1 . . . . 1
  A C E G
   B D F
 6 . . . 6

 4 . B . 4

 2 . . . 2
   B D F
""")

    move_count = game.get_move_count(board)

    assert move_count == 5
