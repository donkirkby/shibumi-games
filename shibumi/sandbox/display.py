from shibumi.sandbox.game import SandboxState
from shibumi.shibumi_display import ShibumiDisplay


class SandboxDisplay(ShibumiDisplay):
    def __init__(self):
        super().__init__(SandboxState())
        self.show_counts = True
        self.show_move_types = True

    def choose_active_text(self):
        return ''
