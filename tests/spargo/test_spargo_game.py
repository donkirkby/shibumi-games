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


def test():
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
