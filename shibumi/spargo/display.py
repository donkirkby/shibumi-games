import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.shibumi_game_state import PlayerCode
from shibumi.spargo.game import SpargoState


class SpargoDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spargo.html'

    def __init__(self, size: int = 4):
        super().__init__(SpargoState(size=size))
        self.visible_counts = PlayerCode.BLACK, PlayerCode.WHITE

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spargo / Margo Game:', 'Cameron Browne'),
                ('Spargo / Margo Implementation:', 'Don Kirkby')]
