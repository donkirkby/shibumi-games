import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spargo.game import SpargoState


class SpargoDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SpargoState())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Shibumi Graphics:', 'Cameron Browne'),
                ('Spargo Game:', 'Cameron Browne'),
                ('Spargo Implementation:', 'Don Kirkby')]
