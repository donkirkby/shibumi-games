import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spook.state import SpookState


class SpookDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SpookState())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spook Game:', 'Dieter Stein'),
                ('Spook Implementation:', 'Don Kirkby')]
