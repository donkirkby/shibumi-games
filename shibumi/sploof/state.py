from copy import copy

import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SploofState(ShibumiGameState):
    game_name = 'Sploof'

    def __init__(self,
                 text: str | None = None,
                 size: int = 4):
        super().__init__(text, size=size)

        levels = self.levels
        if text is None:
            # Starting layout is red around the edges.
            red_type = self.piece_types.index(self.RED)
            levels[red_type, 0, (0, -1), :] = 1
            levels[red_type, 0, 1:-1, (0, -1)] = 1
            player = self.WHITE
            player_stock = 2
            opponent_stock = 2
            self.levels = levels
        else:
            lines = text.splitlines()
            move_line = lines[-1]
            player_text = move_line[1]
            player = self.WHITE if player_text == 'W' else self.BLACK
            stock_text = move_line[3:-1]
            stock_fields = stock_text.split(',')
            player_stock, opponent_stock = (int(stock)
                                            for stock in stock_fields)

        self.active_player = player
        self.player_stock = player_stock
        self.opponent_stock = opponent_stock
        self.winner: typing.Optional[int] = None

    def display(self, show_coordinates: bool = False) -> str:
        text = super().display(show_coordinates)
        player_display = 'W' if self.active_player == self.WHITE else 'B'
        text += f'>{player_display}({self.player_stock},{self.opponent_stock})\n'
        return text

    def display_move(self, move: int) -> str:
        position = move % self.calculate_volume()
        position_display = super().display_move(position)
        if position < move:
            player_display = 'R'
        elif self.get_active_player() == self.WHITE:
            player_display = 'W'
        else:
            player_display = 'B'
        return player_display + position_display

    def get_valid_moves(self) -> np.ndarray:
        size = self.size
        volume = self.calculate_volume(size)
        valid_moves = np.full(2*volume, False)
        # if self.is_win(self.BLACK) or self.is_win(self.WHITE):
        #     return valid_moves

        levels = self.levels
        player_stock = self.player_stock
        if 0 < player_stock:
            self.fill_supported_moves(valid_moves)
        usable_positions = self.get_usable_positions()
        filled_positions = np.logical_and(levels.sum(axis=0),
                                          usable_positions)
        red_type = self.piece_types.index(self.RED)
        red_positions = np.logical_and(levels[red_type],
                                       filled_positions)
        supporting_counts = np.zeros(levels.shape[1:], np.int8)
        supporting_counts[:-1, :, :] += filled_positions[1:, :, :]
        supporting_counts[:-1, 1:, :] += filled_positions[1:, :-1, :]
        supporting_counts[:-1, :, 1:] += filled_positions[1:, :, :-1]
        supporting_counts[:-1, 1:, 1:] += filled_positions[1:, :-1, :-1]
        unpinned_positions = supporting_counts < 2
        unpinned_red: np.ndarray = np.logical_and(red_positions,
                                                  unpinned_positions)

        combined_volume = size * size * size
        usable_indexes = usable_positions.reshape(combined_volume)
        unpinned_red_reshaped = unpinned_red.reshape(combined_volume)
        valid_moves[volume:] = unpinned_red_reshaped[usable_indexes]
        return valid_moves

    def get_active_player(self) -> int:
        return self.active_player

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_state = copy(self)
        new_levels = new_state.levels
        volume = self.calculate_volume(self.size)
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)
        player = new_state.active_player
        new_state.active_player = -player
        old_player_stock = self.player_stock
        new_player_stock = self.opponent_stock
        if move < volume:
            piece_type = self.piece_types.index(player)
            new_levels[piece_type, height, row, column] = 1
            new_state.levels = new_levels
            old_player_stock -= 1
        else:
            new_state.remove(height, row, column)
            old_player_stock += 2
        new_state.player_stock = new_player_stock
        new_state.opponent_stock = old_player_stock
        return new_state

    def get_index(self,
                  height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        position_index = super().get_index(height, row, column)
        if move_type == MoveType.RED:
            return position_index + self.calculate_volume()
        return position_index

    def get_piece_count(self, player: int) -> int:
        if player == self.get_active_player():
            return self.player_stock
        return self.opponent_stock

    def is_win(self, player: int) -> bool:
        if self.winner is not None:
            pass
        elif self.has_line(player):
            self.winner = player
        elif self.has_line(-player):
            self.winner = -player
        else:
            # Not the active player, see if the active player has no valid moves.
            valid_moves = self.get_valid_moves()
            if valid_moves.any():
                self.winner = self.NO_PLAYER
            else:
                # Active player has no valid moves, opponent wins.
                self.winner = -self.get_active_player()
        return self.winner == player

    def has_line(self, player: int) -> bool:
        usable_positions = self.get_usable_positions()
        levels = self.levels
        piece_type = self.piece_types.index(player)
        player_pieces = np.logical_and(levels[piece_type], usable_positions)
        filled_positions = np.logical_and(levels.sum(axis=0),
                                          usable_positions)
        cutoff_pieces = levels[:, 1, :-1, :-1].sum(axis=0)  # Either colour.
        # Count the number of the player's pieces in each row on the base level.
        row_counts = player_pieces[0].sum(1)
        # Zero out any rows that are cut off by pieces crossing over.
        blocked_row_pieces = np.logical_and(cutoff_pieces[:-1, :],
                                            cutoff_pieces[1:, :])
        blocked_rows = blocked_row_pieces.any(1)
        row_counts[1:-1] *= np.logical_not(blocked_rows)
        if (row_counts == 4).any():
            return True
        # Count the number of the player's pieces in each column.
        column_counts = player_pieces[0].sum(0)
        # Zero out any columns that are cut off by pieces crossing over.
        blocked_column_pieces = np.logical_and(cutoff_pieces[:, :-1],
                                               cutoff_pieces[:, 1:])
        blocked_columns = blocked_column_pieces.any(0)
        column_counts[1:-1] *= np.logical_not(blocked_columns)
        if (column_counts == 4).any():
            return True

        # Decide which colour is on top of each position.
        size = self.size
        expanded_size = size * 2 - 1
        top_pieces = np.zeros((expanded_size, expanded_size), bool)
        for height in range(size):
            level_view = top_pieces[height:expanded_size-height:2,
                                    height:expanded_size-height:2]
            level_pieces = player_pieces[height, :size-height, :size-height]
            level_filled = filled_positions[height, :size-height, :size-height]
            level_view[level_filled] = level_pieces[level_filled]
        line_counts1 = np.zeros((expanded_size-3, expanded_size-3), np.int8)
        line_counts2 = np.zeros((expanded_size-3, expanded_size-3), np.int8)
        for i in range(4):
            line_counts1 += top_pieces[i:expanded_size-3+i, i:expanded_size-3+i]
            line_counts2 += top_pieces[3-i:expanded_size-i, i:expanded_size-3+i]
        # noinspection PyUnresolvedReferences
        if (line_counts1 == 4).any():
            return True
        # noinspection PyUnresolvedReferences
        if (line_counts2 == 4).any():
            return True

        return False
