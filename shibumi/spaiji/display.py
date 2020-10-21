from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spaiji.game import SpaijiState


class SpaijiDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SpaijiState())
        self.visible_counts = (self.start_state.BLACK, self.start_state.WHITE)
        self.show_move_types = True
