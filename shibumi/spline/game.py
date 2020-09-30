from shibumi.shibumi_game_state import ShibumiGameState


class SplineState(ShibumiGameState):
    """ Spline game class implementing the zero-play GameState interface. """

    game_name = 'Spline'

    def is_win(self, player: int) -> bool:
        levels = self.get_levels()
        player_pieces = levels == player
        if self.is_straight_winner(player_pieces):
            return True
        if self.is_diagonal_winner(player_pieces):
            return True
        return False

    def is_diagonal_winner(self, player_pieces):
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

    def is_straight_winner(self, player_pieces):
        """Checks if player_pieces contains a vertical or horizontal win."""
        for height in range(self.size):
            level_size = self.size - height
            for row in range(level_size):
                row_pieces = player_pieces[height, row, :level_size]
                if row_pieces.all():
                    return True
            for column in range(level_size):
                row_pieces = player_pieces[height, :level_size, column]
                if row_pieces.all():
                    return True
        return False
