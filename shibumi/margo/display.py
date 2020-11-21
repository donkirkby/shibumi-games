import typing

from shibumi.spargo.display import SpargoDisplay


class MargoDisplay(SpargoDisplay):
    rules_path = ':/shibumi_rules/spargo.html'

    def __init__(self, size: int = 6):
        super().__init__(size=size)

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return []
