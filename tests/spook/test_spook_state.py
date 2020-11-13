from shibumi.spook.state import SpookState


def test_start():
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . . . 1
  A C E G
>R
"""
    state = SpookState()

    display = state.display()
    active_player = state.get_active_player()

    assert display == expected_display
    assert active_player == state.RED


def test_add_move():
    expected_display = """\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . R . 1
  A C E G
>B
"""
    state1 = SpookState()

    state2 = state1.make_move(2)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test():
    state1 = SpookState("""\
  A C E G
7 B B B B 7

5 B B B B 5

3 R R R R 3

1 R R R R 1
  A C E G
   B D F
 6 B B B 6

 4 R R B 4

 2 R R R 2
   B D F
    C E
  5 . B 5

  3 R . 3
    C E
>B
""")
    expected_display = """\
  A C E G
7 B B B B 7

5 B B B B 5

3 R R R R 3

1 R R R R 1
  A C E G
   B D F
 6 B B B 6

 4 R R B 4

 2 R R R 2
   B D F
    C E
  5 B B 5

  3 R R 3
    C E
     D
   4 W 4
     D
>R(B,R)
"""

    state2 = state1.make_move(27)

    display = state2.display()
    active_player = state2.get_active_player()

    assert state1.get_move_count() == 27
    assert state2.get_move_count() == 28
    assert display == expected_display
    assert active_player == state2.RED
