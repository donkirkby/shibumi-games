from shibumi.spargo.game import SpargoState


def test_basic_move():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 W B . . 1
  A C E G
>B
"""

    board2 = board.make_move(0)

    assert board2.display() == expected_board


def test_capture():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 W B . . 1
  A C E G
>B
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 B . . . 3

1 . B . . 1
  A C E G
>W
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_capture_in_top_right():
    board = SpargoState("""\
  A C E G
7 . . B W 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
>B
""")
    expected_board = """\
  A C E G
7 . . B . 7

5 . . . B 5

3 . . . . 3

1 . . . . 1
  A C E G
>W
"""

    board2 = board.make_move(11)

    assert board2.display() == expected_board


def test_connected_to_freedom():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 B B . . 1
  A C E G
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 W . . . 3

1 B B . . 1
  A C E G
>B
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_capture_group():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W . . 3

1 B B W . 1
  A C E G
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 W W . . 3

1 . . W . 1
  A C E G
>B
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_climb_to_freedom():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W B . 3

1 B B W . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . B . 2
   B D F
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 W W B . 3

1 B B W . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . B . 2
   B D F
>B
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_capture_up():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W W . 3

1 B B W . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . B . 2
   B D F
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 W W W . 3

1 . . W . 1
  A C E G
>B
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_zombie():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W W . 3

1 B B W . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . W . 2
   B D F
>W
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 W W W . 3

1 . B W . 1
  A C E G
   B D F
 6 . . . 6

 4 . . . 4

 2 . W . 2
   B D F
>B
"""

    board2 = board.make_move(4)

    assert board2.display() == expected_board


def test_suicide_invalid():
    board = SpargoState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B . . . 3

1 . B . . 1
  A C E G
>W
""")

    valid_moves = board.get_valid_moves()

    is_second_level_valid = valid_moves[16]
    is_bottom_left_valid = valid_moves[0]
    assert not is_second_level_valid
    assert not is_bottom_left_valid


def test_winner():
    board = SpargoState("""\
  A C E G
7 . B B . 7

5 B B B B 5

3 B B B B 3

1 . B B . 1
  A C E G
>W
""")

    assert board.is_ended()
    assert board.is_win(board.BLACK)
    assert not board.is_win(board.WHITE)
    assert board.get_winner() == board.BLACK


def test_draw():
    board = SpargoState("""\
  A C E G
7 . W W . 7

5 W W W W 5

3 B B B B 3

1 . B B B 1
  A C E G
   B D F
 6 . W . 6

 4 W B W 4

 2 . B W 2
   B D F
    C E
  5 . . 5

  3 . B 3
    C E
>B
""")

    assert board.is_ended()
    assert not board.is_win(board.BLACK)
    assert not board.is_win(board.WHITE)
    assert board.get_winner() == board.NO_PLAYER


def test_blocked_player_wins():
    board = SpargoState("""\
  A C E G
7 . W W . 7

5 W W W W 5

3 B B B B 3

1 . B B B 1
  A C E G
   B D F
 6 . W . 6

 4 B W B 4

 2 . B B 2
   B D F
    C E
  5 . . 5

  3 . W 3
    C E
>B
""")

    assert board.is_ended()
    assert board.is_win(board.BLACK)
    assert not board.is_win(board.WHITE)
    assert board.get_winner() == board.BLACK


def test_ko_rule():
    text1 = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W B . 3

1 W B . B 1
  A C E G
>W
"""
    text2 = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . W B . 3

1 W . W B 1
  A C E G
>B
"""

    board1 = SpargoState(text1)
    board2 = board1.make_move(2)

    display = board2.display(show_coordinates=True)
    valid_moves = board2.get_valid_moves()

    assert display == text2
    assert not valid_moves[1]


def test_overpass():
    """ Overpass should cut underpass.

    Playing black at 5G should capture 3G and 1G, because the black overpass
    cuts off their connection to 3C. 3C and 3E survive as zombies, because they
    are supporting pieces on level 2.
    """
    start_state = SpargoState("""\
  A C E G
7 . . . . 7

5 . B B . 5

3 . W W W 3

1 . B B W 1
  A C E G
   B D F
 6 . . . 6

 4 . B . 4

 2 . B . 2
   B D F
>B
""")
    expected_display = """\
  A C E G
7 . . . . 7

5 . B B B 5

3 . W W . 3

1 . B B . 1
  A C E G
   B D F
 6 . . . 6

 4 . B . 4

 2 . B . 2
   B D F
>W
"""

    new_state = start_state.make_move(11)

    display = new_state.display(show_coordinates=True)

    assert display == expected_display
