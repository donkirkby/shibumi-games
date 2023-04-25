from abc import ABC
from enum import IntEnum
import functools

import numpy as np
import typing

from zero_play.game_state import GameState


class PlayerCode(IntEnum):
    WHITE = GameState.O_PLAYER
    BLACK = GameState.X_PLAYER
    NO_PLAYER = GameState.NO_PLAYER
    RED = 2
    UNUSABLE = -2


class MoveType(IntEnum):
    BLACK = PlayerCode.BLACK
    WHITE = PlayerCode.WHITE
    RED = PlayerCode.RED
    REMOVE = 3


class ShibumiGameState(GameState, ABC):
    FIRST_COLUMN_ORD = ord('A')
    RED = int(PlayerCode.RED)
    WHITE = int(PlayerCode.WHITE)
    BLACK = int(PlayerCode.BLACK)
    NO_PLAYER = int(PlayerCode.NO_PLAYER)
    UNUSABLE = int(PlayerCode.UNUSABLE)
    display_characters = {BLACK: 'B',
                          WHITE: 'W',
                          RED: 'R',
                          GameState.NO_PLAYER: '.',
                          UNUSABLE: ' '}

    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 4):
        self.size = size
        if board is None:
            levels = self.UNUSABLE * np.logical_not(self.get_usable_positions())
            board = levels
            if text is not None:
                self.load_text(text, levels)
        self.board = board

    def get_usable_positions(self):
        r = np.arange(self.size, dtype=np.int8)
        heights = r.reshape((self.size, 1, 1))
        rows = r.reshape((1, self.size, 1))
        columns = r.reshape((1, 1, self.size))
        level_sizes = self.size - heights
        is_usablex = np.logical_and(rows < level_sizes, columns < level_sizes)
        return is_usablex

    def __eq__(self, other):
        if not isinstance(other, ShibumiGameState):
            return False
        return np.array_equal(self.board, other.board)

    def load_text(self, text: str, levels: np.ndarray):
        character_players = {
            character: player
            for player, character in self.display_characters.items()}
        lines = text.splitlines()
        for height in range(self.size):
            level_size = self.size - height
            for i in reversed(range(level_size)):
                line_index = (level_size - 1 - i) * 2 + 1
                if line_index >= len(lines):
                    return
                line = lines[line_index]
                for j in range(level_size):
                    character_index = 2 * j + 2 + height
                    if character_index < len(line):
                        character = line[character_index]
                    else:
                        character = '.'
                    try:
                        player = character_players[character]
                    except KeyError as ex:
                        message = f'Unexpected {character!r} at line ' \
                                  f'{line_index+1}, column {character_index+1}.'
                        raise ValueError(message) from ex
                    levels[height, i, j] = player
            lines = lines[level_size*2 + 1:]

    def get_valid_moves(self) -> np.ndarray:
        piece_count = self.calculate_volume(self.size)
        valid_moves = np.full(piece_count, False)
        if self.is_win(self.BLACK) or self.is_win(self.WHITE):
            return valid_moves

        self.fill_supported_moves(valid_moves)
        return valid_moves

    def fill_supported_moves(self, valid_moves: np.ndarray):
        """ Mark any moves that are supported by the board or other pieces.

        :param valid_moves: an array of boolean flags - will be set to True for
            each space that is supported
        """
        levels = self.get_levels()
        piece_index = 0
        for height in range(self.size):
            level_size = self.size - height
            for row in range(level_size):
                for column in range(level_size):
                    if height == 0:
                        is_supported = True
                    else:
                        below_height = height - 1
                        is_supported = all(levels[below_height, lower_row, lower_column] != self.NO_PLAYER
                                           for lower_row in range(row, row + 2)
                                           for lower_column in range(column, column + 2))
                    is_valid = is_supported and levels[height, row, column] == self.NO_PLAYER
                    valid_moves[piece_index] = is_valid
                    piece_index += 1

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def find_possible_neighbours(
            size: int,
            height: int,
            row: int,
            column: int,
            dh_start: int = -1,
            dh_end: int = 2) -> typing.Tuple[typing.Tuple[int, int, int], ...]:
        neighbours = []
        for dh in range(dh_start, dh_end):
            neighbour_height = height + dh
            if not 0 <= neighbour_height < size:
                continue
            for dr in range(-1, 2):
                neighbour_row = row + dr
                if not 0 <= neighbour_row < size - neighbour_height:
                    continue
                for dc in range(-1, 2):
                    neighbour_column = column + dc
                    if not 0 <= neighbour_column < size - neighbour_height:
                        continue
                    if dh == 0:
                        if abs(dr) == abs(dc):
                            continue
                    else:
                        if dh in (dr, dc):
                            continue
                    neighbours.append((neighbour_height,
                                       neighbour_row,
                                       neighbour_column))
        return tuple(neighbours)

    def find_neighbours(self,
                        height: int,
                        row: int,
                        column: int,
                        dh_start: int = -1,
                        dh_end: int = 2) -> typing.Generator[typing.Tuple[int,
                                                                          int,
                                                                          int],
                                                             None,
                                                             None]:
        """ Generate all neighbour positions to the starting position.

        Excludes any that are covered or cut off by overpasses.

        :param height: height of starting position
        :param row: row of starting position
        :param column: column of starting position
        :param dh_start: difference from starting height to start searching. For
            example, 0 means start searching for neighbours at the same height
            as the starting position.
        :param dh_end: difference from ending height to stop searching
            (excluded). For example, 2 means to search one height above the
            starting position, and then stop.
        :return:
        """
        size = self.size
        no_player = int(self.NO_PLAYER)
        possible_neighbours = self.find_possible_neighbours(size,
                                                            height,
                                                            row,
                                                            column,
                                                            dh_start,
                                                            dh_end)
        levels = self.get_levels()
        for (neighbour_height,
             neighbour_row,
             neighbour_column) in possible_neighbours:
            cover_height = neighbour_height + 2
            cover_row = neighbour_row - 1
            cover_column = neighbour_column - 1
            if (0 <= cover_height < size and
                    0 <= cover_row < size - cover_height and
                    0 <= cover_column < size - cover_height):
                cover_piece = (
                    levels[cover_height][cover_row][cover_column])
                if cover_piece != no_player:
                    continue
            if neighbour_height == height:
                overpass_height = neighbour_height + 1
                if overpass_height < size:
                    dr = neighbour_row - row
                    dc = neighbour_column - column
                    if dr:
                        overpass_row1 = overpass_row2 = row + (dr-1) // 2
                        overpass_col1 = column-1
                        overpass_col2 = column
                    else:
                        overpass_row1 = row-1
                        overpass_row2 = row
                        overpass_col1 = overpass_col2 = column + (dc-1) // 2
                    if not (0 <= overpass_col1 and
                            overpass_col2 < size - overpass_height):
                        pass  # Next to the edge, no possible overpass.
                    elif not(0 <= overpass_row1 and
                             overpass_row2 < size - overpass_height):
                        pass  # Next to the edge, no possible overpass.
                    else:
                        overpass_piece1 = levels[overpass_height,
                                                 overpass_row1,
                                                 overpass_col1]
                        overpass_piece2 = levels[overpass_height,
                                                 overpass_row2,
                                                 overpass_col2]
                        if (overpass_piece1 != no_player and
                                overpass_piece2 != no_player):
                            continue
            yield neighbour_height, neighbour_row, neighbour_column

    def calculate_volume(self, base_size: int | None = None):
        if base_size is None:
            base_size = self.size
        return base_size * (base_size + 1) * (2 * base_size + 1) // 6

    def display(self, show_coordinates: bool = False) -> str:
        levels = self.get_levels()
        lines = []
        for height in range(self.size):
            level_pieces = levels[height, :self.size - height, :self.size - height]
            # noinspection PyUnresolvedReferences
            if height > 0 and (level_pieces == self.NO_PLAYER).all():
                break
            level_size = self.size - height
            header = ''
            for column in range(level_size):
                column_name = chr(self.FIRST_COLUMN_ORD + height + column*2)
                header += column_name
            header = ' ' * (height+2) + ' '.join(header)
            lines.append(header)
            for row in reversed(range(level_size)):
                row_name = str(row*2 + 1 + height)
                line = [' ' * height + row_name]
                for column in range(level_size):
                    piece = level_pieces[row, column]
                    line.append(self.display_characters[piece])
                line.append(row_name)
                lines.append(' '.join(line))
                if row:
                    lines.append('')
            lines.append(header)
        lines.append('')
        return '\n'.join(lines)

    def get_levels(self) -> np.ndarray:
        return self.board.reshape((self.size, self.size, self.size))

    def display_move(self, move: int) -> str:
        height, row, column = self.get_coordinates(move)
        return self.display_coordinates(height, row, column)

    @staticmethod
    def display_coordinates(height, row, column):
        row_text = str(height + 1 + 2*row)
        column_text = chr(height + 65 + column*2)
        return row_text + column_text

    def get_move_count(self) -> int:
        """ The number of moves that have already been made in the start_state. """
        pieces = self.exclude_end_spaces()
        return sum(piece in (self.WHITE, self.BLACK)
                   for piece in pieces)

    def get_piece_count(self, player: int) -> int:
        spaces = self.exclude_end_spaces()
        player_count = (spaces == player).sum()
        return player_count

    def exclude_end_spaces(self):
        end_space_count = self.size * self.size - 1
        all_spaces = self.board.reshape(self.size * self.size * self.size)
        spaces = all_spaces[:-end_space_count]
        return spaces

    def get_spaces(self) -> np.ndarray:
        """ Extract the board spaces from the complete game state. """
        return self.get_levels()

    def get_index(self, height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        """ Get the index of a move, based on the details.

        :param height: the height of the move
        :param row: the row of the move
        :param column: the column of the move
        :param move_type: the type of move, for games that allow multiple types
            of moves. Unless a subclass overrides this method, move_type must be
            black.
        :return: the calculated index
        """
        if move_type != MoveType.BLACK:
            raise ValueError(f'Unsupported move type: {move_type!s}.')
        level_size = self.size - height
        level_start = self.calculate_volume(self.size) - self.calculate_volume(level_size)
        return level_start + row*level_size + column

    def get_move_index(self,
                       row_name: str,
                       column_name: str) -> int:
        valid_moves = self.get_valid_moves()
        row = int(row_name) - 1
        row_index = row // 2
        column = ord(column_name.upper()) - self.FIRST_COLUMN_ORD
        column_index = column // 2
        height = row % 2
        while True:
            if height >= self.size:
                break
            if not 0 <= column_index < self.size - height:
                break
            if not 0 <= row_index < self.size - height:
                break
            piece_index = self.get_index(height, row_index, column_index)
            if valid_moves[piece_index]:
                return piece_index
            height += 2
            row_index -= 1
            column_index -= 1
        raise ValueError(f'Invalid move: {row_name}{column_name}.')

    def parse_move(self, text: str) -> int:
        assert len(text) == 2
        row_name, column_name = text[0], text[1]
        return self.get_move_index(row_name, column_name)

    def get_coordinates(self, move_index: int):
        level_index = move_index
        for height in range(self.size):
            level_size = self.size - height
            level_area = level_size * level_size
            if level_index < level_area:
                row = level_index // level_size
                column = level_index % level_size
                return height, row, column
            level_index -= level_area
        raise ValueError(f'Invalid move index: {move_index}.')

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_board = self.__class__(board=self.board.copy())
        levels = new_board.get_levels()
        height, row, column = self.get_coordinates(move)
        player = self.get_active_player()
        levels[height, row, column] = player
        return new_board

    def remove(self, height: int, row: int, column: int):
        upper_height = height+1
        levels = self.board
        for upper_row in (row-1, row):
            if not 0 <= upper_row < self.size - upper_height:
                continue
            for upper_column in (column-1, column):
                if not 0 <= upper_column < self.size - upper_height:
                    continue
                upper_piece = levels[upper_height, upper_row, upper_column]
                if upper_piece != self.NO_PLAYER:
                    levels[height, row, column] = upper_piece
                    self.remove(upper_height, upper_row, upper_column)
                    return
        # No pieces above, just leave this space empty.
        levels[height, row, column] = self.NO_PLAYER

    def is_pinned(self, height: int, row: int, column: int) -> bool:
        support_count = 0
        for height2, row2, column2 in self.find_possible_neighbours(
                self.size,
                height,
                row,
                column,
                dh_start=1):
            neighbour_piece = self.board[height2][row2][column2]
            if neighbour_piece != self.NO_PLAYER:
                support_count += 1
                if support_count > 1:
                    return True  # Supporting more than one neighbour.
        return False

    def is_free(self, height: int, row: int, column: int) -> bool:
        for height2, row2, column2 in self.find_possible_neighbours(
                self.size,
                height,
                row,
                column,
                dh_start=1):
            neighbour_piece = self.board[height2][row2][column2]
            if neighbour_piece != self.NO_PLAYER:
                return False
        return True
