from collections import defaultdict

import numpy as np

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SpaijiState(ShibumiGameState):
    game_name = 'Spaiji'

    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 4):
        if text is None:
            player = self.WHITE
            move_text = ''
        else:
            lines = text.splitlines()
            player_text = lines.pop()
            assert player_text[0] == '>'
            player = self.BLACK if player_text[1] == 'B' else self.WHITE
            move_text = player_text[3:5]
            text = '\n'.join(lines)
        super().__init__(text, board, size)
        if board is not None:
            # Straight copy, don't change anything.
            return
        levels = self.get_levels()
        levels[-1, -1, -1] = player
        if not move_text:
            levels[-1, -1, -2] = -1
        else:
            row_name, column_name = move_text[0], move_text[1]
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
                piece = levels[height, row_index, column_index]
                if piece == self.NO_PLAYER:
                    break
                levels[-1, -1, 0:3] = (height, row_index, column_index)
                height += 2
                row_index -= 1
                column_index -= 1

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player = self.get_active_player()
        player_display = 'W' if player == self.WHITE else 'B'
        levels = self.get_levels()
        last_height, last_row, last_column = levels[-1, -1, 0:3]
        if 0 <= last_column:
            coordinates = self.display_coordinates(last_height,
                                                   last_row,
                                                   last_column)
            player_display += f'({coordinates})'
        display += f'>{player_display}\n'
        return display

    def get_active_player(self) -> int:
        levels = self.get_levels()
        return levels[-1][-1][-1]

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_board = self.__class__(board=self.board.copy())
        levels = new_board.get_levels()
        volume = self.calculate_volume(self.size)
        player = [self.BLACK, self.WHITE][move // volume]
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)
        levels[height, row, column] = player

        old_levels = self.get_levels()
        if old_levels[-1, -1, -2] < 0:
            levels[-1, -1, 0:3] = (height, row, column)
        else:
            levels[-1, -1, -2] = -1
            levels[-1, -1, -1] *= -1
        return new_board

    def get_valid_moves(self) -> np.ndarray:
        volume = self.calculate_volume()
        valid_moves: np.ndarray = np.ndarray(2*volume, bool)
        valid_spaces = valid_moves[:volume]
        self.fill_supported_moves(valid_spaces)
        levels = self.get_levels()
        old_height, old_row, old_column = levels[-1, -1, 0:3]
        if old_column < 0:
            # This is the first move of the turn
            for move, is_valid in enumerate(valid_spaces):
                if is_valid:
                    new_board = self.make_move(move)
                    if not new_board.get_valid_moves().any():
                        # Choosing this move would leave no neighbours to
                        # complete the turn.
                        valid_spaces[move] = False
            # Now copy the same valid moves for white.
            valid_moves[volume:] = valid_spaces
        else:
            old_move_type = levels[old_height, old_row, old_column]
            neighbour_moves = np.zeros(volume, bool)
            for height, row, column in self.find_neighbours(old_height,
                                                            old_row,
                                                            old_column):
                piece = levels[height, row, column]
                if piece == self.NO_PLAYER:
                    move_index = self.get_index(height, row, column)
                    is_valid = valid_spaces[move_index]
                    neighbour_moves[move_index] = is_valid
            if old_move_type == self.WHITE:
                # Now black is valid
                valid_moves[:volume] = neighbour_moves
                valid_moves[volume:] = False
            else:
                # Now white is valid
                valid_moves[:volume] = False
                valid_moves[volume:] = neighbour_moves
        return valid_moves

    def get_index(self, height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        base_move = super().get_index(height, row, column)
        if move_type == self.WHITE:
            base_move += self.calculate_volume()
        return base_move

    def display_move(self, move: int) -> str:
        volume = self.calculate_volume()
        if move < volume:
            colour = 'B'
        else:
            colour = 'W'
            move -= volume
        base_move = super().display_move(move)
        return colour + base_move

    def is_ended(self) -> bool:
        valid_moves = self.get_valid_moves()
        return not valid_moves.any()

    def is_win(self, player: int) -> bool:
        if not self.is_ended():
            return False
        scores = self.get_scores()
        score = scores[player]
        opponent_score = scores[-player]
        if score == opponent_score:
            # Tie goes to second player.
            return player == self.BLACK
        return score > opponent_score

    def get_scores(self):
        levels = self.get_levels()
        if levels[-1, 0, 0] != self.NO_PLAYER:
            unvisited = [(0, 0, 0)]
        else:
            edges = (0, self.size-1)
            unvisited = [(0, row, column)
                         for row in range(self.size)
                         for column in range(self.size)
                         if row in edges or column in edges]

        groups = defaultdict(set)
        while unvisited:
            position = unvisited.pop()
            start_piece = levels[position]
            if start_piece == self.NO_PLAYER:
                continue
            group = groups[position]
            group.add(position)
            for neighbour_position in self.find_neighbours(*position):
                if neighbour_position in groups:
                    continue  # Already seen.
                neighbour_piece = levels[neighbour_position]
                if neighbour_piece == self.NO_PLAYER:
                    continue
                if neighbour_piece != start_piece:
                    # Visit opponent's groups after finishing the current group.
                    unvisited.insert(0, neighbour_position)
                else:
                    group.add(neighbour_position)
                    groups[neighbour_position] = group

                    # Visit next.
                    unvisited.append(neighbour_position)
        scores = {self.WHITE: 0, self.BLACK: 0}
        for position, group in groups.items():
            piece = levels[position]
            group_size = len(group)
            scores[piece] = max(group_size, scores[piece])
        return scores

    def get_piece_count(self, player: int) -> int:
        scores = self.get_scores()
        return scores[player]
