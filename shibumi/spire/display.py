import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spire.state import SpireState
from zero_play.game_state import GameState


class SpireDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spire.html'

    def __init__(self):
        start_state = SpireState()
        super().__init__(start_state)
        self.visible_move_types = (start_state.BLACK,
                                   start_state.RED,
                                   start_state.WHITE)

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, SpireState)

        move_types = game_state.get_valid_colours()
        self.visible_move_types = move_types
        if self.selected_move_type not in move_types:
            self.selected_move_type = move_types[0]
        super().update_board(game_state)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spire Game:', 'Dieter Stein'),
                ('Spire Implementation:', 'Don Kirkby')]
