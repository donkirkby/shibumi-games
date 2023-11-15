from copy import copy

import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState


class IllegalMoveError(Exception):
    """ Raised when a requested move is not allowed. """
    pass


class SpargoState(ShibumiGameState):
    def __init__(self,
                 text: str | None = None,
                 size: int = 4):
        if text is None:
            player = self.BLACK
        else:
            text = text.rstrip()
            player_text = text[-2:]
            if not player_text[0] == '>':
                player = self.BLACK
            else:
                player = self.BLACK if player_text == '>B' else self.WHITE
                text = text[:-2]
        super().__init__(text, size=size)
        self.active_player = player

        # {board.bytes + active_player} for all previous states
        self.history = {self.create_snapshot()}

    def create_snapshot(self):
        snapshot = self.packed.tobytes()
        snapshot += (b'W' if self.active_player == self.WHITE else b'B')
        return snapshot

    @property
    def game_name(self) -> str:
        return 'Spargo' if self.size == 4 else 'Margo'

    def is_ended(self) -> bool:
        valid_moves = self.get_valid_moves()
        return valid_moves.sum() == 0

    def is_win(self, player: int) -> bool:
        if not self.is_ended():
            return False
        player_count = self.get_piece_count(player)
        opponent_count = self.get_piece_count(-player)

        return player_count > opponent_count

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player_display = 'W' if self.active_player == self.WHITE else 'B'
        display += f'>{player_display}\n'
        return display

    def get_active_player(self) -> int:
        return self.active_player

    def make_move(self, move: int) -> 'SpargoState':
        new_state = copy(self)
        new_state.history = self.history.copy()
        levels = new_state.levels
        height, row, column = self.get_coordinates(move)
        player = self.active_player
        other_player = -player
        piece_type = self.piece_types.index(player)
        other_piece_type = self.piece_types.index(other_player)
        levels[piece_type, height, row, column] = 1
        new_state.levels = levels
        captured = set()  # {(height, row, column)}
        for height2, row2, column2 in new_state.find_neighbours(height,
                                                                row,
                                                                column):
            neighbour_piece = levels[:, height2, row2, column2]
            group: typing.Set[typing.Tuple[int, int, int]] = set()
            if (neighbour_piece[other_piece_type] and
                    not new_state.has_freedom(levels,
                                              height2,
                                              row2,
                                              column2,
                                              group)):
                captured |= group

        sorted_capture = sorted(captured, reverse=True)  # Check from top down.
        for height2, row2, column2 in sorted_capture:
            for height3, row3, column3 in new_state.find_possible_neighbours(
                    self.size,
                    height2,
                    row2,
                    column2,
                    dh_start=1):
                piece_above = levels[:, height3, row3, column3]
                if piece_above.sum():
                    break
            else:
                # not supporting any pieces, can be removed.
                levels[:, height2, row2, column2] = 0
        new_state.levels = levels
        if not new_state.has_freedom(levels, height, row, column, set()):
            raise IllegalMoveError('Added piece has no freedom.')
        new_player = other_player
        new_state.active_player = new_player
        new_snapshot = new_state.create_snapshot()
        if new_snapshot in self.history:
            raise IllegalMoveError('Cannot repeat a position.')
        new_state.history.add(new_snapshot)
        return new_state

    def has_freedom(self,
                    levels: np.ndarray,
                    height: int,
                    row: int,
                    column: int,
                    group: set) -> bool:
        """ Check if a ball is connected to a free space on the board.

        :param levels: the board spaces to search
        :param height: the height of the ball to check
        :param row: the row of the ball to check
        :param column: the column of the ball to check
        :param group: coordinates {(height, row, column)} for all balls in the
            same connected group as the ball to check. More connected balls will
            be added until a freedom is found, or no new neighbours can be found.
        :return: True if a freedom is found, otherwise False.
        """
        player = levels[:, height, row, column]
        group.add((height, row, column))
        for neighbour_coordinates in self.find_neighbours(height, row, column):
            height2, row2, column2 = neighbour_coordinates
            neighbour_piece = levels[:, height2, row2, column2]
            if height2 == 0 and neighbour_piece.sum() == 0:
                # Empty space on the board, connected to the group.
                return True
            if (np.array_equal(neighbour_piece, player) and
                    neighbour_coordinates not in group):
                if self.has_freedom(levels, height2, row2, column2, group):
                    return True

        return False

    def get_valid_moves(self,) -> np.ndarray:
        piece_count = self.calculate_volume(self.size)
        valid_moves = np.full(piece_count, False)
        self.fill_supported_moves(valid_moves)
        for move, is_valid in enumerate(valid_moves):
            if not is_valid:
                continue
            try:
                self.make_move(move)
            except IllegalMoveError:
                valid_moves[move] = False

        return valid_moves
