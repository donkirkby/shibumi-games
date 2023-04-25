import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SploofState(ShibumiGameState):
    game_name = 'Sploof'

    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 4):
        super().__init__(text, board, size)

        if board is None:
            board = self.board
            if text is None:
                # Starting layout is red around the edges.
                board[0, (0, -1), :] = self.RED
                board[0, 1:-1, (0, -1)] = self.RED
                player = self.WHITE
                player_stock = 2
                opponent_stock = 2
            else:
                lines = text.splitlines()
                move_line = lines[-1]
                player_text = move_line[1]
                player = self.WHITE if player_text == 'W' else self.BLACK
                stock_text = move_line[3:-1]
                stock_fields = stock_text.split(',')
                player_stock, opponent_stock = (int(stock)
                                                for stock in stock_fields)

            board[-1, -1, -1] = player
            board[-1, -1, -2] = player_stock
            board[-1, -1, -3] = opponent_stock
        self.winner: typing.Optional[int] = None

    def display(self, show_coordinates: bool = False) -> str:
        text = super().display(show_coordinates)
        board = self.board
        player = board[-1, -1, -1]
        player_display = 'W' if player == self.WHITE else 'B'
        player_stock = board[-1, -1, -2]
        opponent_stock = board[-1, -1, -3]
        text += f'>{player_display}({player_stock},{opponent_stock})\n'
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

        board = self.board
        player_stock = board[-1, -1, -2]
        if 0 < player_stock:
            self.fill_supported_moves(valid_moves)
        usable_positions = self.get_usable_positions()
        filled_positions = np.logical_and(board != self.NO_PLAYER,
                                          usable_positions)
        red_positions = np.logical_and(board == self.RED,
                                       filled_positions)
        supporting_counts = np.zeros(board.shape, np.int8)
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
        return self.board[-1, -1, -1]

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_state = self.__class__(board=self.board.copy())
        new_board = new_state.board
        volume = self.calculate_volume(self.size)
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)
        player = new_board[-1, -1, -1]
        new_board[-1, -1, -1] = -player
        old_player_stock = new_board[-1, -1, -2]
        new_player_stock = new_board[-1, -1, -3]
        if move < volume:
            new_board[height, row, column] = player
            old_player_stock -= 1
        else:
            new_state.remove(height, row, column)
            old_player_stock += 2
        new_board[-1, -1, -2] = new_player_stock
        new_board[-1, -1, -3] = old_player_stock
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
            return self.board[-1, -1, -2]
        return self.board[-1, -1, -3]

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
        board = self.board
        player_pieces = np.logical_and(board == player, usable_positions)
        filled_positions = np.logical_and(board != self.NO_PLAYER,
                                          usable_positions)
        cutoff_pieces = board[1, :-1, :-1] != self.NO_PLAYER  # Either colour.
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
        if (line_counts1 == 4).any():
            return True
        if (line_counts2 == 4).any():
            return True

        return False
