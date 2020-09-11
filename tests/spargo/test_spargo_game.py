from shibumi.spargo.game import SpargoGame


def test_basic_move():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 0)

    assert game.display(board2) == expected_board


def test_capture():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_capture_in_top_right():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 11)

    assert game.display(board2) == expected_board


def test_connected_to_freedom():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_capture_group():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_climb_to_freedom():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_capture_up():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_zombie():
    game = SpargoGame()
    board = game.create_board("""\
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

    board2 = game.make_move(board, 4)

    assert game.display(board2) == expected_board


def test_suicide_invalid():
    game = SpargoGame()
    board = game.create_board("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 B . . . 3

1 . B . . 1
  A C E G
>W
""")

    valid_moves = game.get_valid_moves(board)

    is_second_level_valid = valid_moves[16]
    is_bottom_left_valid = valid_moves[0]
    assert not is_second_level_valid
    assert not is_bottom_left_valid


def test_winner():
    game = SpargoGame()
    board = game.create_board("""\
  A C E G
7 . B B . 7

5 B B B B 5

3 B B B B 3

1 . B B . 1
  A C E G
>W
""")

    assert game.is_win(board, game.BLACK)
    assert not game.is_win(board, game.WHITE)
