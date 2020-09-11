import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spline.game import SplineGame


class SplineDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SplineGame())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spline Game:', 'Néstor Romeral Andrés'),
                ('Spline Implementation:', 'Don Kirkby')]
