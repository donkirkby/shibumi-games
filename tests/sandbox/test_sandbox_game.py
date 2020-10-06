from shibumi.sandbox.game import SandboxState


def test_move_black():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B B . 1
  A C E G
"""

    board2 = board.make_move(2)

    assert board2.display() == expected_board


def test_move_white():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")
    expected_board = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B W . 1
  A C E G
"""

    board2 = board.make_move(32)

    assert board2.display() == expected_board


def test_display_move():
    board = SandboxState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . B . . 1
  A C E G
""")

    assert board.display_move(2) == 'B1E'
    assert board.display_move(32) == 'W1E'
