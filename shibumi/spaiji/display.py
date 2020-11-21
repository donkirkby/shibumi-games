import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.shibumi_game_state import MoveType
from shibumi.spaiji.game import SpaijiState
from zero_play.game_state import GameState


class SpaijiDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spaiji.html'

    def __init__(self):
        super().__init__(SpaijiState())
        self.visible_counts = (self.start_state.BLACK, self.start_state.WHITE)
        self.visible_move_types = (MoveType.BLACK, MoveType.WHITE)

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, SpaijiState)
        valid_moves = game_state.get_valid_moves()
        volume = game_state.calculate_volume()
        is_black_valid = valid_moves[:volume].any()
        is_white_valid = valid_moves[volume:].any()
        visible_move_types = []
        if is_black_valid:
            visible_move_types.append(MoveType.BLACK)
        if is_white_valid:
            visible_move_types.append(MoveType.WHITE)
        self.visible_move_types = visible_move_types

        super().update_board(game_state)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Shibumi Graphics:', 'Cameron Browne'),
                ('Spaiji Game:', 'Néstor Romeral Andrés'),
                ('Spaiji Implementation:', 'Don Kirkby')]
