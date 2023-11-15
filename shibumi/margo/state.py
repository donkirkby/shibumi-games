from shibumi.spargo.game import SpargoState


class MargoState(SpargoState):
    def __init__(self,
                 text: str | None = None,
                 size: int = 6):
        super().__init__(text, size)
