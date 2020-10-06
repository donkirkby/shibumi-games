from shibumi.sandbox.game import SandboxState
from shibumi.shibumi_display import ShibumiDisplay


class SandboxDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SandboxState())
        self.show_counts = True
        self.show_colours = True

    def choose_active_text(self):
        return ''

    def make_move(self, move: int):
        assert isinstance(self.current_state, SandboxState)
        volume = self.current_state.calculate_volume()
        if self.selected_colour == SandboxState.WHITE:
            move += volume
        super().make_move(move)
