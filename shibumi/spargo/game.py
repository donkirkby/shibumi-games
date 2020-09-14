import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, PlayerCode


class IllegalMoveError(Exception):
    """ Raised when a requested move is not allowed. """
    pass


class SpargoState(ShibumiGameState):
    game_name = 'Spargo'

    def __init__(self, text: str = None, board: np.ndarray = None):
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
        super().__init__(text, board)
        levels = self.get_levels()
        levels[self.SIZE-1, self.SIZE-1, self.SIZE-1] = player

    def is_ended(self) -> bool:
        valid_moves = self.get_valid_moves()
        return valid_moves.sum() == 0

    def is_win(self, player: int) -> bool:
        if not self.is_ended():
            return False
        player_count = (self.board[:-1] == player).sum()
        opponent_count = (self.board[:-1] == -player).sum()

        return player_count > opponent_count

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player = self.get_active_player()
        player_display = 'W' if player == self.WHITE else 'B'
        display += f'>{player_display}\n'
        return display

    def get_active_player(self) -> int:
        levels = self.get_levels()
        player = PlayerCode(levels[self.SIZE-1, self.SIZE-1, self.SIZE-1])
        if player == self.UNUSABLE:
            player = self.BLACK
        return player

    def make_move(self, move: int) -> 'SpargoState':
        new_board = self.board.copy()
        new_state = SpargoState(board=new_board)
        levels = new_state.get_levels()
        height, row, column = self.get_coordinates(move)
        player = self.get_active_player()
        levels[height, row, column] = player
        captured = set()  # {(height, row, column)}
        for height2, row2, column2 in self.find_neighbours(height, row, column):
            neighbour_piece = levels[height2, row2, column2]
            group: typing.Set[typing.Tuple[int, int, int]] = set()
            if (neighbour_piece not in (player, self.NO_PLAYER) and
                    not self.has_freedom(levels, height2, row2, column2, group)):
                captured |= group

        sorted_capture = sorted(captured, reverse=True)  # Check from top down.
        for height2, row2, column2 in sorted_capture:
            for height3, row3, column3 in self.find_neighbours(height2, row2, column2):
                if height3 != height2 + 1:
                    # Not the level above.
                    continue
                piece_above = levels[height3, row3, column3]
                if piece_above != self.NO_PLAYER:
                    break
            else:
                # not supporting any pieces, can be removed.
                levels[height2, row2, column2] = self.NO_PLAYER
        if not self.has_freedom(levels, height, row, column, set()):
            raise IllegalMoveError('Added piece has no freedom.')
        new_player = self.WHITE if (player == self.BLACK) else self.BLACK
        levels[self.SIZE-1, self.SIZE-1, self.SIZE-1] = new_player
        return new_state

    def find_neighbours(self,
                        height: int,
                        row: int,
                        column: int) -> typing.Generator[typing.Tuple[int,
                                                                      int,
                                                                      int],
                                                         None,
                                                         None]:
        for dh in range(-1, 2):
            neighbour_height = height + dh
            if not 0 <= neighbour_height < self.SIZE:
                continue
            for dr in range(-1, 2):
                neighbour_row = row + dr
                if not 0 <= neighbour_row < self.SIZE - neighbour_height:
                    continue
                for dc in range(-1, 2):
                    neighbour_column = column + dc
                    if not 0 <= neighbour_column < self.SIZE - neighbour_height:
                        continue
                    if dh == 0:
                        if abs(dr) == abs(dc):
                            continue
                    else:
                        if dh in (dr, dc):
                            continue
                    yield neighbour_height, neighbour_row, neighbour_column

    def has_freedom(self,
                    levels: np.ndarray,
                    height: int,
                    row: int,
                    column: int,
                    group: set) -> bool:
        player = levels[height, row, column]
        group.add((height, row, column))
        for neighbour_coordinates in self.find_neighbours(height, row, column):
            height2, row2, column2 = neighbour_coordinates
            neighbour_piece = levels[height2, row2, column2]
            if height2 == 0 and neighbour_piece == self.NO_PLAYER:
                # Empty space on the board, connected to the group.
                return True
            if neighbour_piece == player and neighbour_coordinates not in group:
                if self.has_freedom(levels, height2, row2, column2, group):
                    return True

        return False

    def get_valid_moves(self,) -> np.ndarray:
        piece_count = self.calculate_volume(self.SIZE)
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
