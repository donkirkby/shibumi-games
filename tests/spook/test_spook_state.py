import pytest

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
    assert not state.is_ended()


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


def test_add_last_piece():
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


def test_remove_drop():
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
  5 B B 5

  3 R R 3
    C E
     D
   4 W 4
     D
>R(B,R)
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
  5 B W 5

  3 R R 3
    C E
>B(B,R)
"""

    state2 = state1.make_move(28)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test_remove_only_neighbour():
    """ One neighbour on same level with no more of that colour. """
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
  5 B W 5

  3 R R 3
    C E
>B(B,R)
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
  5 W . 5

  3 R R 3
    C E
>R(B,R)
"""

    state2 = state1.make_move(27)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.RED


def test_remove_first_neighbour():
    """ One neighbour on same level with another of that colour. """
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
  5 B W 5

  3 R R 3
    C E
>B(B,R)
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
  5 B . 5

  3 R W 3
    C E
>B(R)
"""

    state2 = state1.make_move(26)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test_remove_only_free_neighbour():
    """ One neighbour on same level with no more of that colour. """
    state1 = SpookState("""\
  A C E G
7 B B . . 7

5 B B B W 5

3 . . . . 3

1 . . . . 1
  A C E G
   B D F
 6 R . . 6

 4 . . . 4

 2 . . . 2
   B D F
>B(B,R)
""")
    expected_display = """\
  A C E G
7 B B . . 7

5 B B W . 5

3 . . . . 3

1 . . . . 1
  A C E G
   B D F
 6 R . . 6

 4 . . . 4

 2 . . . 2
   B D F
>R(B,R)
"""

    state2 = state1.make_move(10)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.RED


def test_move_ghost():
    state1 = SpookState("""\
  A C E G
7 B B . R 7

5 B B . . 5

3 . . . . 3

1 W . . . 1
  A C E G
>R(B,R)
""")
    expected_display = """\
  A C E G
7 B B . R 7

5 B B . W 5

3 . . . . 3

1 . . . . 1
  A C E G
>B(B,R)
"""

    state2 = state1.make_move(11)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test_remove_opponent_piece():
    state1 = SpookState("""\
  A C E G
7 B B B . 7

5 R R R . 5

3 W . . . 3

1 . . . R 1
  A C E G
   B D F
 6 B R . 6

 4 . . . 4

 2 . . . 2
   B D F
>B(B,R)
""")
    expected_display = """\
  A C E G
7 B B B . 7

5 R R R . 5

3 W . . . 3

1 . . . R 1
  A C E G
   B D F
 6 B . . 6

 4 . . . 4

 2 . . . 2
   B D F
>R(B,R)
"""

    state2 = state1.make_move(23)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.RED


def test_remove_opponent_piece_with_free_neighbour():
    state1 = SpookState("""\
  A C E G
7 B B . . 7

5 R R . . 5

3 W . . R 3

1 . . . R 1
  A C E G
   B D F
 6 B . . 6

 4 . . . 4

 2 . . . 2
   B D F
>B(B,R)
""")
    expected_display = """\
  A C E G
7 B B . . 7

5 R R . . 5

3 W . . R 3

1 . . . . 1
  A C E G
   B D F
 6 B . . 6

 4 . . . 4

 2 . . . 2
   B D F
>R(B,R)
"""

    state2 = state1.make_move(3)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.RED


def test_pass():
    state1 = SpookState("""\
  A C E G
7 B B . R 7

5 B B . . 5

3 . . . . 3

1 W R . . 1
  A C E G
>R(R)
""")
    expected_display = """\
  A C E G
7 B B . R 7

5 B B . . 5

3 . . . . 3

1 W R . . 1
  A C E G
>B(B,R)
"""

    state2 = state1.make_move(30)

    display = state2.display()
    active_player = state2.get_active_player()

    assert display == expected_display
    assert active_player == state2.BLACK


def test_getaway_move_count():
    state = SpookState("""\
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

  3 R W 3
    C E
>B(B,R)
""")
    expected_move_count = 29

    assert state.get_move_count() == expected_move_count


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 2, True, 'empty spaces'),
                          (2, 3, False, 'already occupied'),
                          (3, 16, True, 'empty spaces'),
                          (16, 30, False, 'no support'),
                          (30, 31, False, 'no passing in adding phase')])
def test_valid_adds(start: int, end: int, expected_valid: bool, reason: str):
    board = SpookState("""\
  A C E G
7 . . . . 7

5 . . . . 5

3 . . . . 3

1 . . R . 1
  A C E G
>B
""")
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 31  # 30 adds, plus pass
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 16, False, "not close to ghost"),
                          (16, 18, True, 'drop'),
                          (18, 19, False, 'not close'),
                          (19, 21, False, 'pinned'),
                          (21, 25, False, 'not close'),
                          (25, 26, False, "can't remove ghost"),
                          (26, 27, False, "empty space"),
                          (27, 28, True, "move ghost to neighbour"),
                          (28, 29, False, "not close"),
                          (29, 30, False, "above ghost"),
                          (30, 31, False, "can't pass until you've moved")])
def test_valid_removes(start: int, end: int, expected_valid: bool, reason: str):
    board = SpookState("""\
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

  3 W . 3
    C E
>R(B,R)
""")
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 31  # 30 removes, plus pass
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 9, False, "not close to ghost"),
                          (9, 11, False, "pinned"),
                          (11, 13, False, "not close"),
                          (13, 14, False, "pinned"),
                          (14, 15, True, "drop"),
                          (15, 20, False, "not close"),
                          (20, 21, True, "red neighbour"),
                          (21, 22, False, "not close"),
                          (22, 23, True, "black neighbour"),
                          (23, 24, False, "can't remove ghost"),
                          (24, 30, False, "above ghost"),
                          (30, 31, False, "can't pass until you've moved")])
def test_valid_removes_any_colour(start: int,
                                  end: int,
                                  expected_valid: bool,
                                  reason: str):
    board = SpookState("""\
  A C E G
7 B B B B 7

5 B B B B 5

3 R R R R 3

1 R R R R 1
  A C E G
   B D F
 6 B W . 6

 4 R R B 4

 2 R R R 2
   B D F
>R(B,R)
""")
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 31  # 30 removes, plus pass
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 9, False, "not close to ghost"),
                          (9, 11, False, "pinned"),
                          (11, 13, False, "not close"),
                          (13, 14, False, "pinned"),
                          (14, 15, False, "drop not allowed after turn starts"),
                          (15, 20, False, "not close"),
                          (20, 21, False, "red neighbour"),
                          (21, 22, False, "not close"),
                          (22, 23, True, "black neighbour"),
                          (23, 24, False, "can't remove ghost"),
                          (24, 30, False, "above ghost"),
                          (30, 31, True, "can pass when you've moved")])
def test_valid_removes_black(start: int,
                             end: int,
                             expected_valid: bool,
                             reason: str):
    board = SpookState("""\
  A C E G
7 B B B B 7

5 B B B B 5

3 R R R R 3

1 R R R R 1
  A C E G
   B D F
 6 B W . 6

 4 R R B 4

 2 R R R 2
   B D F
>R(B)
""")
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 31  # 30 removes, plus pass
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 5, False, "empty spaces"),
                          (5, 6, False, "can't remove ghost"),
                          (6, 7, True, "red neighbour"),
                          (7, 9, False, "not close to ghost"),
                          (9, 10, False, "not free"),
                          (10, 30, False, "not close"),
                          (30, 31, False, "can't pass until you've moved")])
def test_valid_remove_only_free(start: int,
                                end: int,
                                expected_valid: bool,
                                reason: str):
    board = SpookState("""\
  A C E G
7 B B . . 7

5 B B . . 5

3 . W R . 3

1 . . . . 1
  A C E G
   B D F
 6 B . . 6

 4 . . . 4

 2 . . . 2
   B D F
>R(B,R)
""")
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 31  # 30 removes, plus pass
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 1, False, "can't remove ghost"),
                          (1, 4, False, "no neighbours"),
                          (4, 6, True, "neighbour"),
                          (6, 8, False, "no neighbours"),
                          (8, 10, False, "occupied"),
                          (10, 12, True, "neighbour"),
                          (12, 14, False, "occupied"),
                          (14, 15, True, "two neighbours"),
                          (15, 16, False, "occupied"),
                          (16, 22, False, "unsupported"),
                          (22, 23, True, "supported"),
                          (23, 30, False, "unsupported"),
                          (30, 31, False, "can't pass until you've moved")])
def test_valid_ghost(start: int, end: int, expected_valid: bool, reason: str):
    board = SpookState("""\
  A C E G
7 B B . R 7

5 B B . . 5

3 . . . . 3

1 W . . . 1
  A C E G
>R(B,R)
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


@pytest.mark.parametrize('start,end,expected_valid,reason',
                         [(0, 3, False, "empty"),
                          (3, 4, True, "remove opponent"),
                          (4, 5, False, "can't remove ghost"),
                          (5, 8, False, "empty"),
                          (8, 9, True, "opponent"),
                          (9, 10, False, "pinned"),
                          (10, 11, True, "opponent"),
                          (11, 12, False, "empty"),
                          (12, 15, False, "can't remove own pieces"),
                          (15, 22, False, "empty"),
                          (22, 23, False, "own piece"),
                          (23, 24, True, "opponent"),
                          (24, 30, False, "empty"),
                          (30, 31, False, "can't pass until you've moved")])
def test_valid_none_free(start: int, end: int, expected_valid: bool, reason: str):
    """ Ghost has neighbours, but none are free.

    Valid moves are to remove opponent pieces.
    """
    board = SpookState("""\
  A C E G
7 B B B . 7

5 R R R . 5

3 W . . . 3

1 . . . R 1
  A C E G
   B D F
 6 B R . 6

 4 . . . 4

 2 . . . 2
   B D F
>B(B,R)
""")
    valid_moves = board.get_valid_moves()
    for move in range(start, end):
        assert valid_moves[move] == expected_valid, move


def test():
    state = SpookState("""\
  A C E G
7 . . . . 7

5 . . B W 5

3 . . . . 3

1 . . . . 1
  A C E G
>B(B,R)
""")

    assert not state.is_win(state.BLACK)
    assert state.is_win(state.RED)
    assert state.get_winner() == state.RED
    assert state.is_ended()


def test_display_pass():
    state = SpookState()

    move_display = state.display_move(30)

    assert move_display == 'PASS'


def test_display_move():
    state = SpookState()

    move_display = state.display_move(0)

    assert move_display == '1A'
