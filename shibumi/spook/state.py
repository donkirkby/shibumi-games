import numpy as np

from shibumi.shibumi_game_state import ShibumiGameState, PlayerCode


class SpookState(ShibumiGameState):
    game_name = 'Spook'

    def __init__(self,
                 text: str = None,
                 board: np.ndarray = None,
                 size: int = 4):
        super().__init__(text, board, size)
        if board is None:
            if text is None:
                active_player = self.RED
            else:
                lines = text.splitlines()
                move_line = lines[-1]
                active_player = self.RED if move_line[1] == 'R' else self.BLACK
            spaces = self.board.reshape(self.size*self.size*self.size)[:-3]
            # noinspection PyUnresolvedReferences
            black_count = (spaces == self.BLACK).sum()
            # noinspection PyUnresolvedReferences
            red_count = (spaces == self.RED).sum()

            # Extras, reversed: active player, move count, restricted colour
            self.board[-1, -1, -1] = active_player
            self.board[-1, -1, -2] = black_count + red_count
            self.board[-1, -1, -3] = self.UNUSABLE
            # Restricted colour:
            # - UNUSABLE means we're still adding
            # - NO_PLAYER means you can remove either colour
            # - RED or BLACK means you can only remove that colour

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player_display = 'R' if self.get_active_player() == self.RED else 'B'
        restricted_colour = self.board[-1, -1, -3]
        if restricted_colour == self.UNUSABLE:
            allowed_display = ''
        elif restricted_colour == self.NO_PLAYER:
            allowed_display = '(B,R)'
        else:
            colour_name = PlayerCode(restricted_colour).name[0]
            allowed_display = f'({colour_name})'

        display += f'>{player_display}{allowed_display}\n'
        return display

    def get_active_player(self) -> int:
        return self.board[-1, -1, -1]

    def make_move(self, move: int) -> 'ShibumiGameState':
        new_state = super().make_move(move)
        player = self.get_active_player()
        new_player = self.BLACK if player == self.RED else self.RED
        new_board = new_state.board
        new_board[-1, -1, -1] = new_player
        move_count = self.get_move_count() + 1
        volume = self.calculate_volume()
        if move_count == volume - 2:
            height = self.size - 2
            for row in range(2):
                for column in range(2):
                    if new_board[height, row, column] == self.NO_PLAYER:
                        new_board[height, row, column] = new_player

                        # Add ghost on top
                        new_board[height+1, 0, 0] = self.WHITE

                        # No restriction on colour to remove
                        new_board[-1, -1, -3] = self.NO_PLAYER
                        break
        new_board[-1, -1, -2] = move_count
        return new_state

    def get_move_count(self) -> int:
        return self.board[-1, -1, -2]

    def is_win(self, player: int) -> bool:
        return False
