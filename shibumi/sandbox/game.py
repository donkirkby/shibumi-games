import numpy as np

from shibumi.shibumi_game_state import ShibumiGameState, MoveType


class SandboxState(ShibumiGameState):
    game_name = 'Sandbox'

    def is_win(self, player: int) -> bool:
        return False

    def get_active_player(self) -> int:
        return self.NO_PLAYER

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_board = self.__class__(board=self.board.copy())
        levels = new_board.get_levels()
        volume = self.calculate_volume(self.size)
        player = [self.BLACK,
                  self.WHITE,
                  self.RED,
                  self.NO_PLAYER][move // volume]
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)
        if player != self.NO_PLAYER:
            levels[height, row, column] = player
        else:
            new_board.remove(height, row, column)
        return new_board

    def get_valid_moves(self) -> np.ndarray:
        valid_spaces = super().get_valid_moves()
        volume = self.calculate_volume(self.size)
        valid_moves: np.ndarray = np.ndarray(volume*4, dtype=bool)
        for section in range(3):
            valid_moves[section*volume:(section+1)*volume] = valid_spaces

        # Removal section
        section_start = volume*3
        levels = self.get_levels()
        for move_index in range(volume):
            height, row, column = self.get_coordinates(move_index)
            existing_piece = levels[height][row][column]
            if existing_piece == self.NO_PLAYER:
                is_valid = False
            else:
                # Piece found, see if it's supporting any neighbours above.
                is_valid = not self.is_pinned(height, row, column)
            valid_moves[section_start+move_index] = is_valid
        return valid_moves

    def get_index(self,
                  height: int,
                  row: int = 0,
                  column: int = 0,
                  move_type: MoveType = MoveType.BLACK):
        base_index = super().get_index(height, row, column)
        section = [MoveType.BLACK,
                   MoveType.WHITE,
                   MoveType.RED,
                   MoveType.REMOVE].index(move_type)
        volume = self.calculate_volume(self.size)
        return section * volume + base_index

    def display_move(self, move: int) -> str:
        volume = self.calculate_volume()
        section = move // volume
        move_type = [MoveType.BLACK,
                     MoveType.WHITE,
                     MoveType.RED,
                     MoveType.REMOVE][section]
        prefix = 'x' if move_type == MoveType.REMOVE else move_type.name[0]
        position_index = move % volume
        base_display = super().display_move(position_index)

        return prefix + base_display
