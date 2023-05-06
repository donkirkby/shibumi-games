from textwrap import dedent

import pytest

from shibumi.sparks.state import SparksState


def test_start():
    expected_display = dedent("""\
          A C E G
        7 W B W B 7
        
        5 B W B W 5
        
        3 W B W B 3
        
        1 B W B W 1
          A C E G
        <W
        """)
    state = SparksState()

    display = state.display()
    active_player = state.get_active_player()

    assert display == expected_display
    assert active_player == state.WHITE


@pytest.mark.parametrize('move_index,expected_display,expected_valid',
                         [(16, '2B', False),
                          (0, '1A', False),
                          (1, '1C', True)])
def test_display_take_move(move_index: int,
                           expected_display: str,
                           expected_valid: bool):
    state = SparksState()

    display = state.display_move(move_index)

    assert display == expected_display

    valid_moves = state.get_valid_moves()
    assert valid_moves[move_index] == expected_valid


@pytest.mark.parametrize('move_index,expected_display,expected_valid',
                         [(46, 'R2B', True),
                          (16, 'B2B', True),
                          (0, 'B1A', False),
                          (1, 'B1C', False)])
def test_display_add_move(move_index: int,
                          expected_display: str,
                          expected_valid: bool):
    state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
        >B, R
        """))

    display = state.display_move(move_index)

    assert display == expected_display

    valid_moves = state.get_valid_moves()
    assert valid_moves[move_index] == expected_valid


@pytest.mark.parametrize('move_index,expected_display,expected_valid',
                         [(46, 'R2B', True),
                          (16, 'B2B', False),
                          (0, 'B1A', False),
                          (1, 'B1C', False)])
def test_display_add_red_move(move_index: int,
                              expected_display: str,
                              expected_valid: bool):
    state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
        >R
        """))

    display = state.display_move(move_index)

    assert display == expected_display

    valid_moves = state.get_valid_moves()
    assert valid_moves[move_index] == expected_valid


@pytest.mark.parametrize('move_index,expected_display,expected_valid',
                         [(46, 'R2B', False),
                          (16, 'W2B', True),
                          (0, 'W1A', False),
                          (1, 'W1C', False)])
def test_display_add_white_move(move_index: int,
                                expected_display: str,
                                expected_valid: bool):
    state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 B R B W 1
          A C E G
        >W
        """))

    display = state.display_move(move_index)

    assert display == expected_display

    valid_moves = state.get_valid_moves()
    assert valid_moves[move_index] == expected_valid


@pytest.mark.parametrize('move_index,expected_display,expected_valid',
                         [(16, '2B', True),
                          (0, '1A', False),
                          (4, '3A', False)])
def test_display_take_pinned_move(move_index: int,
                                  expected_display: str,
                                  expected_valid: bool):
    state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W R 3

        1 B W B R 1
          A C E G
           B D F
         6 . . . 6
         
         4 B . . 4
         
         2 W . . 2
           B D F
        <W
        """))

    display = state.display_move(move_index)

    assert display == expected_display

    valid_moves = state.get_valid_moves()
    assert valid_moves[move_index] == expected_valid

    # Make sure you can't take red moves.
    assert not valid_moves[35]


def test_take_first():
    start_state = SparksState()
    move_index = start_state.parse_move('1C')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 B R B W 1
          A C E G
        >W
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display


def test_place_first():
    start_state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 B R B W 1
          A C E G
        >W
        """))
    move_index = start_state.parse_move('2B')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 B R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . . . 4
         
         2 W . . 2
           B D F
        <B
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display


def test_take_second():
    start_text = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 B R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . . . 4
         
         2 W . . 2
           B D F
        <B
        """)
    start_state = SparksState(start_text, move_count=2)
    move_index = start_state.parse_move('3C')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
        >B, R
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display
    assert state.get_move_count() == 3


def test_take_spark_drop():
    start_text = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B W B 3

        1 W R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . . . 4
         
         2 B R . 2
           B D F
        <W
        """)
    start_state = SparksState(start_text, move_count=2)
    move_index = start_state.parse_move('3E')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W B R B 3

        1 W R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . . . 4
         
         2 B . . 2
           B D F
        >W
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display
    assert state.get_move_count() == 3


def test_place_second_black():
    start_text = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
        >B, R
        """)
    start_state = SparksState(start_text, move_count=3)
    move_index = start_state.parse_move('B4D')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . B . 4
         
         2 . . . 2
           B D F
        >R
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display
    assert state.get_move_count() == 4


def test_place_second_red():
    start_state = SparksState(dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
        >B, R
        """))
    move_index = start_state.parse_move('R4D')
    expected_display = dedent("""\
          A C E G
        7 W B W B 7

        5 B W B W 5

        3 W W W B 3

        1 B R B W 1
          A C E G
           B D F
         6 . . . 6
         
         4 . R . 4
         
         2 . . . 2
           B D F
        >B
        """)

    state = start_state.make_move(move_index)

    assert state.display() == expected_display


def test_white_win():
    state = SparksState(dedent("""\
          A C E G
        7 R R R R 7

        5 R W B B 5

        3 R W W B 3

        1 R R R R 1
          A C E G
           B D F
         6 R W B 2
         
         4 B W B 4
         
         2 R R W 2
           B D F
            C E
          5 W B 5
          
          3 B R 3
            C E
             D
           4 W 4
             D
        <B
        """))

    assert not state.is_win(state.BLACK)
    assert state.is_win(state.WHITE)


def test_black_win():
    state = SparksState(dedent("""\
          A C E G
        7 R R R R 7

        5 R W B B 5

        3 R W W B 3

        1 R R R R 1
          A C E G
           B D F
         6 R W B 2
         
         4 B W B 4
         
         2 R R W 2
           B D F
            C E
          5 W B 5
          
          3 W R 3
            C E
        >B
        """))

    assert not state.is_win(state.BLACK)

    state2 = state.make_move(29)
    assert not state.is_win(state.WHITE)

    assert not state2.is_win(state.WHITE)
    assert state2.is_win(state.BLACK)


def test_all_pinned():
    state = SparksState(dedent("""\
          A C E G
        7 W B W R 7

        5 B R R R 5

        3 R B W B 3

        1 R B B W 1
          A C E G
           B D F
         6 R R W 2
         
         4 B B R 4
         
         2 R W R 2
           B D F
            C E
          5 R W 5
          
          3 W . 3
            C E
        <B
        """))

    assert state.get_piece_count(state.WHITE) == 8
    assert state.get_piece_count(state.RED) == 12
    assert state.get_piece_count(state.BLACK) == 8
    assert state.is_win(state.WHITE)
    assert not state.is_win(state.BLACK)
