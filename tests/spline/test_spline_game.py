# noinspection PyPackageRequirements
import pytest

from shibumi.spline.game import SplineState


def test_start_display():
    board = SplineState()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
"""

    display = board.display(show_coordinates=True)

    assert display == expected_display


def test_start_valid_moves():
    board = SplineState()
    expected_moves = [True] * 16 + [False] * 14

    valid_moves = board.get_valid_moves()

    assert valid_moves.tolist() == expected_moves


def test_add_stone_display():
    board1 = SplineState()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""

    move = board1.parse_move('3E')
    board2 = board1.make_move(move)
    display = board2.display(show_coordinates=True)

    assert display == expected_display


def test_add_stone_lower_case():
    board1 = SplineState()
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""

    move = board1.parse_move('3e')
    board2 = board1.make_move(move)
    display = board2.display(show_coordinates=True)

    assert display == expected_display


def test_init_text():
    expected_display = """\
  A C E G
7 . . . . 7

5 . W . . 5

3 . . B . 3

1 . . . . 1
  A C E G
"""
    board = SplineState(text=expected_display)

    display = board.display(show_coordinates=True)

    assert display == expected_display


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
    board = SplineState(text=expected_display)

    display = board.display(show_coordinates=True)

    assert display == expected_display


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
    board = SplineState(text=text)

    display = board.display(show_coordinates=True)

    assert display == expected_display


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
        SplineState(text=text)


def test_add_stone_second_level():
    board1 = SplineState("""\
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

    move = board1.parse_move('4D')
    board2 = board1.make_move(move)
    display = board2.display(show_coordinates=True)

    assert display == expected_display


def test_add_stone_third_level():
    board1 = SplineState("""\
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

    move = board1.parse_move('5e')
    board2 = board1.make_move(move)
    display = board2.display(show_coordinates=True)

    assert display == expected_display


def test_add_stone_occupied_row():
    board1 = SplineState("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 5C.'):
        board1.parse_move('5C')


def test_add_stone_bad_column():
    board1 = SplineState("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 5X.'):
        board1.parse_move('5X')


def test_add_stone_bad_row():
    board1 = SplineState("""\
  A C E G
7 . . . . 7

5 . W B . 5

3 . W B . 3

1 . . . . 1
  A C E G
""")

    with pytest.raises(ValueError, match='Invalid move: 9C.'):
        board1.parse_move('9C')


def test_full_spaces_valid_moves():
    board = SplineState("""\
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

    assert valid_moves.tolist() == expected_valid_moves


def test_second_level_valid_moves():
    board = SplineState("""\
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

    assert valid_moves.tolist() == expected_valid_moves


def test_win_row():
    board = SplineState("""\
  A C E G
7 . . . . 7

5 W W W W 5

3 . B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = board.WHITE

    winner = board.get_winner()

    assert winner == expected_winner


def test_win_column():
    board = SplineState("""\
  A C E G
7 W W B . 7

5 W W B W 5

3 W B B . 3

1 . B B . 1
  A C E G
""")
    expected_winner = board.BLACK

    winner = board.get_winner()

    assert winner == expected_winner


def test_win_column_level_2():
    board = SplineState("""\
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
    expected_winner = board.WHITE

    winner = board.get_winner()

    assert winner == expected_winner


def test_win_diagonal():
    board = SplineState("""\
  A C E G
7 W W B . 7

5 W W B B 5

3 W B W B 3

1 . B B W 1
  A C E G
""")
    expected_winner = board.WHITE

    winner = board.get_winner()

    assert winner == expected_winner


def test_valid_moves_after_win():
    board = SplineState("""\
  A C E G
7 . W B . 7

5 . W B . 5

3 . W B . 3

1 . . B . 1
  A C E G
""")
    expected_valid_moves = [False] * 30

    valid_moves = board.get_valid_moves()

    assert expected_valid_moves == valid_moves.tolist()


def test_get_levels():
    board = SplineState("""\
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
    w = board.WHITE
    b = board.BLACK
    n = board.NO_PLAYER
    u = board.UNUSABLE
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
    assert board.get_levels().tolist() == expected_levels


@pytest.mark.parametrize(['move_index', 'expected_display'],
                         [(0, '1A'),
                          (3, '1G'),
                          (4, '3A'),
                          (16, '2B')])
def test_display_move(move_index: int, expected_display: str):
    board = SplineState("""\
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

    display = board.display_move(move_index)

    assert display == expected_display


def test_get_move_count():
    board = SplineState("""\
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

    move_count = board.get_move_count()

    assert move_count == 5
