import typing

import shibumi
from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spline.game import SplineState


class SplineDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spline.html'

    def __init__(self):
        super().__init__(SplineState())

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Spline Game:', 'Néstor Romeral Andrés'),
                ('Spline Implementation:', 'Don Kirkby'),
                ('Shibumi Version', shibumi.__version__)]
