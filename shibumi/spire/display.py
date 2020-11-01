from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spire.state import SpireState
from zero_play.game_state import GameState


class SpireDisplay(ShibumiDisplay):
    def __init__(self):
        start_state = SpireState()
        super().__init__(start_state)
        self.visible_move_types = (start_state.BLACK,
                                   start_state.RED,
                                   start_state.WHITE)

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, SpireState)
        super().update_board(game_state)

        self.visible_move_types = game_state.get_valid_colours()
