import typing

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spline.game import SplineState


class SplineDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spline.md'

    def __init__(self):
        super().__init__(SplineState())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spline Game:', 'Néstor Romeral Andrés'),
                ('Spline Implementation:', 'Don Kirkby')]
