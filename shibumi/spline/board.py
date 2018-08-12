from collections import namedtuple
from enum import IntEnum

# noinspection PyPackageRequirements
import numpy as np


class Player(IntEnum):
    UNUSABLE = -2
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
                          Player.NONE: '.',
                          Player.UNUSABLE: ' '}

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

        piece_count = self.calculate_volume(size)
        if pieces is not None:
            self.pieces = pieces
            self.levels = self.pieces.reshape((size, size, size))
        else:
            self.pieces = None
            self.levels = None
            self.init_pieces()
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
                    is_valid = is_supported and self.levels[height, row, column] == Player.NONE
                    self.valid_moves[piece_index] = is_valid
                    piece_index += 1

    def init_pieces(self):
        r = np.arange(self.size, dtype=np.int8)
        heights = r.reshape(self.size, 1, 1)
        rows = r.reshape(1, self.size, 1)
        columns = r.reshape(1, 1, self.size)
        level_sizes = self.size - heights
        self.levels = Player.UNUSABLE * np.logical_or(rows >= level_sizes,
                                                      columns >= level_sizes)
        self.pieces = self.levels.reshape(self.size*self.size//2, self.size*2)

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
                    self.levels[height, i, j] = player
            lines = lines[level_size*2 + 1:]

    def get_spaces_count(self):
        return (self.levels != Player.UNUSABLE).sum()

    def get_index(self, height, row=0, column=0):
        level_size = self.size - height
        level_start = self.calculate_volume(self.size) - self.calculate_volume(level_size)
        return level_start + row*level_size + column

    def get_coordinates(self, move_index):
        for height in range(self.size):
            level_size = self.size - height
            level_area = level_size * level_size
            if move_index < level_area:
                row = move_index // level_size
                column = move_index % level_size
                return height, row, column
            move_index -= level_area

    @staticmethod
    def calculate_volume(base_size):
        return base_size * (base_size + 1) * (2 * base_size + 1) // 6

    def get_stone(self, height, row, column):
        return self.levels[height, row, column]

    def make_move(self, piece_index, player):
        height, row, column = self.get_coordinates(piece_index)
        self.levels[height, row, column] = player

    def add_stone(self, row_name, column_name, player):
        move_index = self.get_move_index(row_name, column_name)
        self.make_move(move_index, player)

    def get_move_index(self, row_name, column_name):
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
            if self.valid_moves[piece_index]:
                return piece_index
            height += 2
            row_index -= 1
            column_index -= 1
        raise ValueError(f'Invalid move: {row_name}{column_name}.')

    def get_valid_moves(self):
        return self.valid_moves

    def get_winner(self):
        for player in [Player.BLACK, Player.WHITE]:
            player_pieces = self.levels == player
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
            level_pieces = player_pieces[height, :level_size, :level_size]
            diagonal_pieces = level_pieces.diagonal()
            if diagonal_pieces.all():
                return True
            if level_size > 1:
                diagonal_pieces = level_pieces[-1::-1].diagonal()
                if diagonal_pieces.all():
                    return True
        return False

    def _is_straight_winner(self, player_pieces):
        """Checks if player_pieces contains a vertical or horizontal win."""
        for height in range(self.size):
            level_size = self.size - height
            level_pieces = player_pieces[height, :level_size, :level_size]
            for row in range(level_size):
                row_pieces = player_pieces[height, row, :level_size]
                if row_pieces.all():
                    return True
            for column in range(level_size):
                row_pieces = player_pieces[height, :level_size, column]
                if row_pieces.all():
                    return True
        return False

    def __str__(self):
        lines = []
        for height in range(self.size):
            level_pieces = self.levels[height, :self.size-height, :self.size-height]
            if height > 0 and (level_pieces == Player.NONE).all():
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
