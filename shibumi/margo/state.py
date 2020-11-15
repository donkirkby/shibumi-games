import typing

import numpy as np

from shibumi.spargo.game import SpargoState


class MargoState(SpargoState):
    def __init__(self,
                 text: str = None,
                 board: np.ndarray = None,
                 size: int = 6,
                 history: typing.Set[bytes] = None):
        super().__init__(text, board, size, history)
