from shibumi.shibumi_game_state import ShibumiGameState


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
        player = [self.BLACK, self.WHITE, self.RED][move // volume]
        position_index = move % volume
        height, row, column = self.get_coordinates(position_index)
        levels[height, row, column] = player
        return new_board

    def display_move(self, move: int) -> str:
        volume = self.calculate_volume()
        colour = 'W' if move // volume else 'B'
        position_index = move % volume
        base_display = super().display_move(position_index)

        return colour + base_display
