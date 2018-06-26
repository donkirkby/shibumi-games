from collections import namedtuple
from enum import IntEnum

# noinspection PyPackageRequirements
import numpy as np


class Player(IntEnum):
    BLACK = -1
    NONE = 0
    WHITE = 1
    RED = 2


WinState = namedtuple('WinState', 'is_ended winner')


class Board:
    """
    Spline Board.
    """
    FIRST_COLUMN_ORD = ord('A')
    display_characters = {Player.BLACK: 'B',
                          Player.WHITE: 'W',
                          Player.RED: 'R',
                          Player.NONE: '.'}

    def __init__(self,
                 size=4,
                 text=None,
                 pieces=None):
        """ Set up initial board configuration.

        :param size: board width and height
        :param text: starting state as a display string
        :param pieces: starting state as a numpy array
        """
        self.size = size

        piece_count = 0
        for i in range(1, size+1):
            piece_count += i*i
        self.pieces = (pieces if pieces is not None
                       else np.full(piece_count, Player.NONE, np.int8))
        if text is not None:
            self.load(text)
        self.valid_moves = np.full(piece_count, False)
        piece_index = 0
        for height in range(self.size):
            level_size = self.size - height
            for row in range(level_size):
                for column in range(level_size):
                    if height == 0:
                        is_supported = True
                    else:
                        below_height = height-1
                        is_supported = all(self.get_stone(below_height, lower_row, lower_column) != Player.NONE
                                           for lower_row in range(row, row+2)
                                           for lower_column in range(column, column+2))
                    is_valid = is_supported and self.pieces[piece_index] == Player.NONE
                    self.valid_moves[piece_index] = is_valid
                    piece_index += 1

    def load(self, text):
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
                    self.pieces[self.get_index(height, i, j)] = player
            lines = lines[level_size*2 + 1:]

    def get_spaces_count(self):
        return len(self.pieces)

    def get_index(self, height, row=0, column=0):
        level_size = self.size - height
        level_start = len(self.pieces) - level_size*(level_size+1)*(2*level_size+1) // 6
        return level_start + row*level_size + column

    def get_stone(self, height, row, column):
        return self.pieces[self.get_index(height, row, column)]

    def make_move(self, piece_index, player):
        self.pieces[piece_index] = player

    def add_stone(self, row_name, column_name, player):
        move_index = self.get_move_index(row_name, column_name)
        self.make_move(move_index, player)

    def get_move_index(self, row_name, column_name):
        row = int(row_name) - 1
        row_index = row // 2
        column = ord(column_name) - self.FIRST_COLUMN_ORD
        column_index = column // 2
        height = row % 2
        while True:
            piece_index = self.get_index(height, row_index, column_index)
            if self.valid_moves[piece_index]:
                return piece_index
            height += 2
            if height >= self.size:
                raise ValueError(f'Invalid move: {row_name}{column_name}.')
            row_index -= 1
            column_index -= 1

    def get_valid_moves(self):
        return self.valid_moves

    def get_winner(self):
        for player in [Player.BLACK, Player.WHITE]:
            player_pieces = self.pieces == player
            if self._is_straight_winner(player_pieces):
                return player
            if self._is_diagonal_winner(player_pieces):
                return player

    def with_np_pieces(self, np_pieces):
        """Create copy of board with specified pieces."""
        if np_pieces is None:
            np_pieces = self.pieces
        return Board(self.size, pieces=np_pieces)

    def _is_diagonal_winner(self, player_pieces):
        """Checks if player_pieces contains a diagonal win."""
        for height in range(self.size):
            level_size = self.size - height
            level_start = self.get_index(height)
            diagonal_start = level_start
            diagonal_end = diagonal_start + level_size*level_size
            diagonal_pieces = player_pieces[diagonal_start:diagonal_end:level_size+1]
            if diagonal_pieces.all():
                return True
            if level_size > 1:
                diagonal_start = level_start + level_size-1
                diagonal_end = level_start + level_size*level_size - 1
                diagonal_pieces = player_pieces[diagonal_start:diagonal_end:level_size-1]
                if diagonal_pieces.all():
                    return True
        return False

    def _is_straight_winner(self, player_pieces):
        """Checks if player_pieces contains a vertical or horizontal win."""
        for height in range(self.size):
            level_size = self.size - height
            level_start = self.get_index(height)
            for row in range(level_size):
                row_start = level_start + row * level_size
                row_pieces = player_pieces[row_start:row_start + level_size]
                if row_pieces.all():
                    return True
            for column in range(level_size):
                column_start = level_start + column
                column_end = column_start + level_size*level_size
                row_pieces = player_pieces[column_start:column_end:level_size]
                if row_pieces.all():
                    return True
        return False

    def __str__(self):
        lines = []
        for i in range(self.size):
            level_pieces = self.pieces[self.get_index(i):self.get_index(i+1)]
            if i > 0 and (level_pieces == Player.NONE).all():
                break
            level_size = self.size - i
            header = ''
            for column in range(level_size):
                column_name = chr(self.FIRST_COLUMN_ORD + i + column*2)
                header += column_name
            header = ' ' * (i+2) + ' '.join(header)
            lines.append(header)
            for row in reversed(range(level_size)):
                row_name = str(row*2 + 1 + i)
                line = [' ' * i + row_name]
                for column in range(level_size):
                    piece = level_pieces[row*level_size + column]
                    line.append(self.display_characters[piece])
                line.append(row_name)
                lines.append(' '.join(line))
                if row:
                    lines.append('')
            lines.append(header)
        lines.append('')
        return '\n'.join(lines)
