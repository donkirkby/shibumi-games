import numpy as np

from zero_play.game import Game


class SplineGame(Game):
    """
    Spline Game class implementing the alpha-zero-general Game interface.
    """
    SIZE = 4
    UNUSABLE = -2
    BLACK = Game.X_PLAYER
    WHITE = Game.O_PLAYER
    RED = 2
    FIRST_COLUMN_ORD = ord('A')
    display_characters = {BLACK: 'B',
                          WHITE: 'W',
                          RED: 'R',
                          Game.NO_PLAYER: '.',
                          UNUSABLE: ' '}

    name = 'Spline'

    def create_board(self, text: str = None) -> np.ndarray:
        r = np.arange(self.SIZE, dtype=np.int8)
        heights = r.reshape((self.SIZE, 1, 1))
        rows = r.reshape((1, self.SIZE, 1))
        columns = r.reshape((1, 1, self.SIZE))
        level_sizes = self.SIZE - heights
        levels = self.UNUSABLE * np.logical_or(rows >= level_sizes,
                                               columns >= level_sizes)
        if text is not None:
            self.load_text(text, levels)
        pieces = levels.reshape(self.SIZE*self.SIZE//2, self.SIZE*2)
        return pieces

    def load_text(self, text: str, levels: np.ndarray):
        character_players = {
            character: player
            for player, character in self.display_characters.items()}
        lines = text.splitlines()
        for height in range(self.SIZE):
            level_size = self.SIZE - height
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

    def get_valid_moves(self, board: np.ndarray) -> np.ndarray:
        levels = self.get_levels(board)
        piece_count = self.calculate_volume(self.SIZE)
        valid_moves = np.full(piece_count, False)
        piece_index = 0
        for height in range(self.SIZE):
            level_size = self.SIZE - height
            for row in range(level_size):
                for column in range(level_size):
                    if height == 0:
                        is_supported = True
                    else:
                        below_height = height-1
                        is_supported = all(levels[below_height, lower_row, lower_column] != self.NO_PLAYER
                                           for lower_row in range(row, row+2)
                                           for lower_column in range(column, column+2))
                    is_valid = is_supported and levels[height, row, column] == self.NO_PLAYER
                    valid_moves[piece_index] = is_valid
                    piece_index += 1
        return valid_moves

    @staticmethod
    def calculate_volume(base_size):
        return base_size * (base_size + 1) * (2 * base_size + 1) // 6

    def display(self, board: np.ndarray, show_coordinates: bool = False) -> str:
        levels = self.get_levels(board)
        lines = []
        for height in range(self.SIZE):
            level_pieces = levels[height, :self.SIZE-height, :self.SIZE-height]
            # noinspection PyUnresolvedReferences
            if height > 0 and (level_pieces == self.NO_PLAYER).all():
                break
            level_size = self.SIZE - height
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

    def get_levels(self, board) -> np.ndarray:
        levels = board.reshape(self.SIZE, self.SIZE, self.SIZE)
        return levels

    def display_move(self, board: np.ndarray, move: int) -> str:
        height, row, column = self.get_coordinates(move)
        row_text = str(height + 1 + 2*row)
        column_text = chr(height + 65 + column*2)
        return row_text + column_text

    def get_move_count(self, board: np.ndarray) -> int:
        """ The number of moves that have already been made in the game. """
        raise NotImplementedError()

    def get_spaces(self, board: np.ndarray) -> np.ndarray:
        """ Extract the board spaces from the complete game state. """
        raise NotImplementedError()

    def get_index(self, height, row=0, column=0):
        level_size = self.SIZE - height
        level_start = self.calculate_volume(self.SIZE) - self.calculate_volume(level_size)
        return level_start + row*level_size + column

    def get_move_index(self,
                       board: np.ndarray,
                       row_name: str,
                       column_name: str) -> int:
        valid_moves = self.get_valid_moves(board)
        row = int(row_name) - 1
        row_index = row // 2
        column = ord(column_name.upper()) - self.FIRST_COLUMN_ORD
        column_index = column // 2
        height = row % 2
        while True:
            if height >= self.SIZE:
                break
            if not 0 <= column_index < self.SIZE - height:
                break
            if not 0 <= row_index < self.SIZE - height:
                break
            piece_index = self.get_index(height, row_index, column_index)
            if valid_moves[piece_index]:
                return piece_index
            height += 2
            row_index -= 1
            column_index -= 1
        raise ValueError(f'Invalid move: {row_name}{column_name}.')

    def parse_move(self, text: str, board: np.ndarray) -> int:
        assert len(text) == 2
        row_name, column_name = text[0], text[1]
        return self.get_move_index(board, row_name, column_name)

    def get_coordinates(self, move_index):
        for height in range(self.SIZE):
            level_size = self.SIZE - height
            level_area = level_size * level_size
            if move_index < level_area:
                row = move_index // level_size
                column = move_index % level_size
                return height, row, column
            move_index -= level_area

    def make_move(self, board: np.ndarray, move: int) -> np.ndarray:
        new_board = board.copy()
        levels = self.get_levels(new_board)
        height, row, column = self.get_coordinates(move)
        player = self.get_active_player(board)
        levels[height, row, column] = player
        return new_board

    def is_win(self, board: np.ndarray, player: int) -> bool:
        levels = self.get_levels(board)
        player_pieces = levels == player
        if self.is_straight_winner(player_pieces):
            return True
        if self.is_diagonal_winner(player_pieces):
            return True
        return False

    def is_diagonal_winner(self, player_pieces):
        """Checks if player_pieces contains a diagonal win."""
        for height in range(self.SIZE):
            level_size = self.SIZE - height
            level_pieces = player_pieces[height, :level_size, :level_size]
            diagonal_pieces = level_pieces.diagonal()
            if diagonal_pieces.all():
                return True
            if level_size > 1:
                diagonal_pieces = level_pieces[-1::-1].diagonal()
                if diagonal_pieces.all():
                    return True
        return False

    def is_straight_winner(self, player_pieces):
        """Checks if player_pieces contains a vertical or horizontal win."""
        for height in range(self.SIZE):
            level_size = self.SIZE - height
            for row in range(level_size):
                row_pieces = player_pieces[height, row, :level_size]
                if row_pieces.all():
                    return True
            for column in range(level_size):
                row_pieces = player_pieces[height, :level_size, column]
                if row_pieces.all():
                    return True
        return False
