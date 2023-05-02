from shibumi.shibumi_display import ShibumiDisplay
from shibumi.shibumi_game_state import MoveType
from shibumi.sparks.state import SparksState
from zero_play.game_state import GameState


class SparksDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/sparks.html'

    def __init__(self):
        super().__init__(SparksState())
        self.visible_move_types = (MoveType.REMOVE, )
        self.visible_counts = (MoveType.RED, )

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, SparksState)
        player = game_state.get_active_player()
        player_move = MoveType(player)
        visible_move_types = []
        if not game_state.is_adding:
            visible_move_types.append(MoveType.REMOVE)
        else:
            if game_state.has_coal:
                visible_move_types.append(player_move)
            if game_state.has_spark:
                visible_move_types.append(MoveType.RED)
        self.visible_move_types = tuple(visible_move_types)
        super().update_board(game_state)
