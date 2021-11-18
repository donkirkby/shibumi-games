import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spook.state import SpookState
from zero_play.game_state import GameState


class SpookDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spook.html'

    def __init__(self):
        super().__init__(SpookState())
        self.ui.pass_button.clicked.connect(self.make_pass_move)

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, SpookState)
        super().update_board(game_state)
        valid_moves = game_state.get_valid_moves()
        volume = game_state.calculate_volume()
        is_pass_valid = bool(valid_moves[volume])
        self.ui.pass_button.setVisible(is_pass_valid)

    def make_pass_move(self):
        volume = self.start_state.calculate_volume()
        self.make_move(volume)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spook Game:', 'Dieter Stein'),
                ('Spook Implementation:', 'Don Kirkby')]
