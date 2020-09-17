import typing

from PySide2.QtGui import QResizeEvent, Qt

from shibumi.shibumi_display import ShibumiDisplay
from shibumi.spargo.game import SpargoState
from zero_play.game_display import center_text_item
from zero_play.game_state import GameState


class SpargoDisplay(ShibumiDisplay):
    rules_path = ':/shibumi_rules/spargo.md'

    def __init__(self):
        super().__init__(SpargoState())
        scene = self.scene()
        self.small_black_item = scene.addPixmap(self.black_pixmap)
        self.small_white_item = scene.addPixmap(self.white_pixmap)
        self.black_count = scene.addSimpleText('0')
        self.white_count = scene.addSimpleText('0')
        self.black_count_x = self.white_count_x = self.count_y = 0

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        small_size = self.black_scaled.width() // 2
        small_black = self.black_pixmap.scaled(small_size,
                                               small_size,
                                               Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation)
        small_white = self.white_pixmap.scaled(small_size,
                                               small_size,
                                               Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation)
        self.small_black_item.setPixmap(small_black)
        self.small_white_item.setPixmap(small_white)
        x0 = self.background_item.x()
        y0 = self.background_item.y()
        large_size = self.background_item.pixmap().width()
        self.small_black_item.setPos(x0+large_size*81//80, y0+large_size//9)
        self.small_white_item.setPos(x0+large_size*91//80, y0+large_size//9)
        self.count_y = y0 + large_size*55//200
        self.black_count_x = x0 + large_size*86//80
        self.white_count_x = x0 + large_size*96//80
        font = self.move_text.font()
        self.black_count.setFont(font)
        self.white_count.setFont(font)
        self.update_count_text()

    # noinspection DuplicatedCode
    def update_count_text(self):
        assert isinstance(self.current_state, SpargoState)
        black_count = self.current_state.get_piece_count(
            self.current_state.BLACK)
        white_count = self.current_state.get_piece_count(
            self.current_state.WHITE)
        self.black_count.setText(f'{black_count}')
        self.white_count.setText(f'{white_count}')
        center_text_item(self.black_count, self.black_count_x, self.count_y)
        center_text_item(self.white_count, self.white_count_x, self.count_y)

    def update_board(self, game_state: GameState):
        super().update_board(game_state)
        self.update_count_text()

    @property
    def credit_pairs(self) -> typing.Iterable[typing.Tuple[str, str]]:
        return [('Shibumi Graphics:', 'Cameron Browne'),
                ('Spargo Game:', 'Cameron Browne'),
                ('Spargo Implementation:', 'Don Kirkby')]
