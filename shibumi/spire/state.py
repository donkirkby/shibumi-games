import typing
from itertools import product

import numpy as np

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SpireState(ShibumiGameState):
    game_name = 'Spire'

    def __init__(self, text: str | None = None, board: np.ndarray | None = None):
        """ Initialize a board state.

        :param text: a text representation, like that from display()
        :param board: a copy of the board state from another instance; the last
            position holds the current player, and the second last is RED if a
            red ball has not been played this turn, and NO_PLAYER if one has
        """
        move_line = None
        if text is not None:
            lines = text.splitlines()
            if lines[-1].startswith('>'):
                move_line = lines.pop()
                text = '\n'.join(lines)
        super().__init__(text, board)
        if board is None:
            if move_line is None:
                player = self.BLACK
                red_move = self.RED
            else:
                if move_line[1] == 'B':
                    player = self.BLACK
                else:
                    player = self.WHITE
                if len(move_line) > 2:
                    red_move = self.RED
                else:
                    red_move = self.NO_PLAYER
            self.board[-1, -1, -1] = player
            self.board[-1, -1, -2] = red_move
        self.winner = self.NO_PLAYER
        self.is_end_checked = False

    def display(self, show_coordinates: bool = False) -> str:
        text = super().display(show_coordinates)
        board = self.board
        player = board[-1, -1, -1]
        is_red_allowed = board[-1, -1, -2] == self.RED
        player_display = 'W' if player == self.WHITE else 'B'
        red_display = ',R' if is_red_allowed else ''
        text += f'>{player_display}{red_display}\n'
        return text

    def display_move(self, move: int) -> str:
        move_space = move % self.calculate_volume()
        space_display = super().display_move(move_space)
        if move_space != move:
            colour_display = 'R'
        elif self.get_active_player() == self.BLACK:
            colour_display = 'B'
        else:
            colour_display = 'W'
        return colour_display + space_display

    def get_active_player(self) -> int:
        return self.board[-1, -1, -1]

    def get_valid_moves(self) -> np.ndarray:
        volume = self.calculate_volume(self.size)
        valid_moves: np.ndarray = np.ndarray(volume * 2, bool)
        player_moves = valid_moves[:volume]
        self.fill_supported_moves(player_moves)

        board = self.board
        player = board[-1, -1, -1]
        red_move = board[-1, -1, -2]
        if red_move == self.NO_PLAYER:
            valid_moves[volume:] = False
        else:
            red_moves = valid_moves[volume:]
            valid_moves[volume:] = player_moves
            self.check_colour_matches(red_moves, self.RED)

        self.check_colour_matches(player_moves, player)
        if not valid_moves.any():
            self.winner = -player
        self.is_end_checked = True
        return valid_moves

    def check_colour_matches(self, valid_moves: np.ndarray, colour: int):
        levels = self.get_levels()
        size = self.size
        match_counts: np.ndarray = np.ndarray(levels.shape, np.int8)
        indexes = self.get_used_indexes(size)
        # Look for matching neighbours within each 2x2 square.
        # delta = dst - src
        for dr in (-1, 1):
            src_row1 = (1 + dr) // 2
            src_row2 = size - (1 - dr) // 2
            dst_row1 = (1 - dr) // 2
            dst_row2 = size - (1 + dr) // 2
            for dc in (-1, 1):
                src_col1 = (1 + dc) // 2
                src_col2 = size - (1 - dc) // 2
                dst_col1 = (1 - dc) // 2
                dst_col2 = size - (1 + dc) // 2
                match_counts.fill(0)
                match_counts[:, dst_row1:dst_row2, :] += \
                    levels[:, src_row1:src_row2, :] == colour
                match_counts[:, :, dst_col1:dst_col2] += \
                    levels[:, :, src_col1:src_col2] == colour
                match_counts[:, dst_row1:dst_row2, dst_col1:dst_col2] += \
                    levels[:, src_row1:src_row2, src_col1:src_col2] == colour
                valid_moves &= match_counts.reshape(size * size * size)[indexes] < 2
        # Look for matching neighbours supporting each point on higher levels.
        match_counts.fill(0)
        match_counts[1:size, :, :] += levels[0:size - 1, :, :] == colour
        match_counts[1:size, 0:size - 1, :] += \
            levels[0:size - 1, 1:size, :] == colour
        match_counts[1:size, :, 0:size - 1] += \
            levels[0:size - 1, :, 1:size] == colour
        match_counts[1:size, 0:size - 1, 0:size - 1] += \
            levels[0:size - 1, 1:size, 1:size] == colour
        valid_moves &= match_counts.reshape(size * size * size)[indexes] < 2

    @staticmethod
    def get_used_indexes(size):
        nums = list(range(size))
        indexes = [h * size * size + r * size + c
                   for (h, r, c) in product(nums, nums, nums)
                   if (r < size - h and c < size - h)]
        return indexes

    def is_win(self, player: int) -> bool:
        if not self.is_end_checked:
            self.get_valid_moves()
        return player == self.winner

    def make_move(self, move: int) -> 'ShibumiGameState':
        volume = self.calculate_volume()
        player = self.get_active_player()
        if move // volume:
            move_colour = self.RED
            next_player = player
            next_red = self.NO_PLAYER
        else:
            move_colour = player
            next_player = -player
            next_red = self.RED
        move_space = move % volume
        new_board = self.__class__(board=self.board.copy())
        levels = new_board.get_levels()
        height, row, column = self.get_coordinates(move_space)
        levels[height, row, column] = move_colour
        levels[-1, -1, -1] = next_player
        levels[-1, -1, -2] = next_red
        return new_board

    def get_valid_colours(self) -> typing.Tuple[MoveType, ...]:
        board = self.board
        player = board[-1, -1, -1]
        if board[-1, -1, -2] == self.RED:
            return MoveType(player), MoveType(self.RED)
        return MoveType(player),

    def get_index(self, height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        position_index = super().get_index(height, row, column)
        if move_type == self.RED:
            return position_index + self.calculate_volume()
        return position_index

    def get_coordinates(self, move_index: int):
        position_index = move_index % self.calculate_volume()
        return super().get_coordinates(position_index)
