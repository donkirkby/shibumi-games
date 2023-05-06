import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SparksState(ShibumiGameState):
    game_name = 'Sparks'

    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 4,
                 move_count: int = 0):
        super().__init__(text, board, size)

        if board is None:
            board = self.board
            self.set_move_count(move_count)
            if text is None:
                # Starting layout is a checkerboard of white and black.
                board[0, 0::2, 1::2] = self.WHITE
                board[0, 1::2, ::2] = self.WHITE
                board[0, 0::2, ::2] = self.BLACK
                board[0, 1::2, 1::2] = self.BLACK
                player = self.WHITE
                self.is_adding = False
            else:
                lines = text.splitlines()
                move_line = lines[-1]
                player_text = move_line[1]
                self.is_adding = move_line[0] == '>'
                if self.is_adding:
                    self.has_spark = move_line[-1] == 'R'
                    self.has_coal = move_line[1] != 'R'
                player = self.WHITE if player_text == 'W' else self.BLACK

            self.set_active_player(player)
        self.winner: typing.Optional[int] = None

    def get_active_player(self) -> int:
        return self.board[-1, -1, -1]

    def set_active_player(self, player: int):
        self.board[-1, -1, -1] = player

    def get_move_count(self) -> int:
        return self.board[-1, -1, -2]

    def set_move_count(self, move_count: int):
        self.board[-1, -1, -2] = move_count

    @property
    def is_adding(self):
        return self.board[-1, -1, -3]

    @is_adding.setter
    def is_adding(self, is_adding: bool):
        self.board[-1, -1, -3] = is_adding

    @property
    def has_coal(self):
        return self.board[-1, -1, -4]

    @has_coal.setter
    def has_coal(self, has_coal: bool):
        self.board[-1, -1, -4] = has_coal

    @property
    def has_spark(self):
        return self.board[-1, -2, -1]

    @has_spark.setter
    def has_spark(self, has_spark: bool):
        self.board[-1, -2, -1] = has_spark

    def display(self, show_coordinates: bool = False) -> str:
        text = super().display(show_coordinates)
        prefix = '>' if self.is_adding else '<'
        active_colours = []
        player = self.get_active_player()
        player_colour = 'W' if player == self.WHITE else 'B'
        if not self.is_adding:
            active_colours.append(player_colour)
        else:
            if self.has_coal:
                active_colours.append(player_colour)
            if self.has_spark:
                active_colours.append('R')
        active_display = ', '.join(active_colours)
        text += f'{prefix}{active_display}\n'
        return text

    def parse_move(self, text: str) -> int:
        if len(text) != 3:
            to_add = ''
        else:
            to_add = text[0]
            text = text[1:]
        move_index = super().parse_move(text)
        if to_add == 'R':
            move_index += self.calculate_volume()
        return move_index

    def display_move(self, move: int) -> str:
        position = move % self.calculate_volume()
        position_display = super().display_move(position)

        if not self.is_adding:
            return position_display

        if position < move:
            player_display = 'R'
        elif self.get_active_player() == self.WHITE:
            player_display = 'W'
        else:
            player_display = 'B'
        return player_display + position_display

    def get_index(self,
                  height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        base_move = super().get_index(height, row, column)
        if move_type == self.RED:
            base_move += self.calculate_volume()
        return base_move

    def get_valid_moves(self) -> np.ndarray:
        size = self.size
        volume = self.calculate_volume(size)
        valid_moves = np.full(2*volume, False)

        if self.is_adding:
            self.fill_supported_moves(valid_moves)
            if self.has_spark:
                valid_moves[volume:] = valid_moves[:volume]
            if not self.has_coal:
                valid_moves[:volume] = False
        else:
            player = self.get_active_player()
            player_pieces = self.board == player
            for height, row, column in np.argwhere(player_pieces):
                if height == size-1 and row > 0:
                    # Outside valid spaces.
                    continue
                if self.is_pinned(height, row, column):
                    continue
                move = self.get_index(height, row, column)
                valid_moves[move] = True

        return valid_moves

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_state = self.__class__(board=self.board.copy())
        new_board = new_state.board
        new_move_count = self.get_move_count() + 1
        new_state.set_move_count(new_move_count)
        volume = self.calculate_volume(self.size)
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)

        if self.is_adding:
            player = self.get_active_player()
            if move < volume:
                to_add = player
                new_state.has_coal = False
            else:
                to_add = self.RED
                new_state.has_spark = False
            new_board[height, row, column] = to_add
            if new_state.has_spark or new_state.has_coal:
                new_state.is_adding = True
            else:
                new_state.set_active_player(-player)
                new_state.is_adding = False
        else:
            new_state.remove(height, row, column)
            replaced_by = new_board[height, row, column]
            if replaced_by == self.NO_PLAYER:
                new_board[height, row, column] = self.RED
                new_state.has_spark = False
            else:
                new_state.has_spark = replaced_by != self.RED
            new_state.has_coal = True
            new_state.is_adding = True
        return new_state

    def is_win(self, player: int) -> bool:
        if self.board[3, 0, 0] in (self.BLACK, self.WHITE):
            return self.board[3, 0, 0] == player
        if not self.get_valid_moves().any():
            return player != self.get_active_player()
        return False
