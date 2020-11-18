import numpy as np

from shibumi.shibumi_game_state import ShibumiGameState


class SploofState(ShibumiGameState):
    game_name = 'Sploof'

    def __init__(self,
                 text: str = None,
                 board: np.ndarray = None,
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

    def display(self, show_coordinates: bool = False) -> str:
        text = super().display(show_coordinates)
        board = self.board
        player = board[-1, -1, -1]
        player_display = 'W' if player == self.WHITE else 'B'
        player_stock = board[-1, -1, -2]
        opponent_stock = board[-1, -1, -3]
        text += f'>{player_display}({player_stock},{opponent_stock})\n'
        return text

    def get_valid_moves(self) -> np.ndarray:
        size = self.size
        volume = self.calculate_volume(size)
        valid_moves = np.full(2*volume, False)
        # if self.is_win(self.BLACK) or self.is_win(self.WHITE):
        #     return valid_moves

        self.fill_supported_moves(valid_moves)
        board = self.board
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

    def is_win(self, player: int) -> bool:
        return False
