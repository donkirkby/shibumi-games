from shibumi.shibumi_display import ShibumiDisplay
from shibumi.shibumi_game_state import MoveType
from shibumi.sploof.state import SploofState
from zero_play.game_state import GameState


class SploofDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/sploof.html'

    def __init__(self):
        super().__init__(SploofState())
        self.visible_counts = (self.start_state.WHITE, self.start_state.BLACK)

    def update_board(self, game_state: GameState):
        player = game_state.get_active_player()
        player_move = MoveType(player)
        self.visible_move_types = (player_move, MoveType.RED)
        super().update_board(game_state)