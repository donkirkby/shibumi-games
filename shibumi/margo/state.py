import typing

import numpy as np

from shibumi.spargo.game import SpargoState


class MargoState(SpargoState):
    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 6,
                 history: typing.Set[bytes] | None = None):
        super().__init__(text, board, size, history)
