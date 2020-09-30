import typing
from math import floor

from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap, QFont, QResizeEvent, QPainter
from PySide2.QtWidgets import (QGraphicsPixmapItem, QGraphicsSceneHoverEvent,
                               QGraphicsSceneMouseEvent)

from shibumi.shibumi_game_state import ShibumiGameState
from zero_play.game_display import GameDisplay, center_text_item
from zero_play.game_state import GameState
from shibumi import shibumi_images_rc
from shibumi import shibumi_rules_rc

assert shibumi_images_rc  # Need to import this module to load resources.
assert shibumi_rules_rc  # Need to import this module to load resources.


class GraphicsShibumiPieceItem(QGraphicsPixmapItem):
    def __init__(self, height: int, row: int, column: int, hover_listener=None):
        super().__init__()
        self.height = height
        self.row = row
        self.column = column
        self.setAcceptHoverEvents(True)
        self.hover_listener = hover_listener

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverEnterEvent(event)
        self.hover_listener.on_hover_enter(self)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverLeaveEvent(event)
        self.hover_listener.on_hover_leave(self)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.hover_listener.on_click(self)

    def __repr__(self):
        return (f'GraphicsShibumiPieceItem({self.height}, {self.row}, '
                f'{self.column})')


class ShibumiDisplay(GameDisplay):
    def __init__(self, start_state: ShibumiGameState):
        super().__init__(start_state)
        self.start_state = start_state
        self.background_pixmap = self.assemble_board()
        scene = self.scene()
        self.background_item = scene.addPixmap(self.background_pixmap)
        self.white_scaled = self.white_pixmap = self.load_pixmap(
            'ball-w-shadow-1.png')
        self.black_scaled = self.black_pixmap = self.load_pixmap(
            'ball-b-shadow-1.png')
        self.black_player = self.black_pixmap
        self.white_player = self.white_pixmap
        self.item_levels = []
        for height in range(self.start_state.size):
            item_level = []
            for row in range(self.start_state.size - height):
                item_row = []
                for column in range(self.start_state.size - height):
                    item = GraphicsShibumiPieceItem(height, row, column, self)
                    scene.addItem(item)
                    item_row.append(item)
                item_level.append(item_row)
            self.item_levels.append(item_level)
        self.row_labels = []
        self.column_labels = []
        for i in range(self.start_state.size * 2 - 1):
            self.row_labels.append(scene.addSimpleText(str(i + 1)))
            self.column_labels.append(scene.addSimpleText(chr(i + 65)))
        self.player_item = scene.addPixmap(QPixmap())
        self.move_text = scene.addSimpleText('')
        self.text_x = self.text_y = 0
        self.debug_message = ''

    def assemble_board(self) -> QPixmap:
        full_board = self.load_pixmap('board-1.png')
        board_size = self.start_state.size
        if board_size == 4:
            return full_board
        full_height = full_board.height()
        full_width = full_board.width()
        left_width = round(full_width * 0.28)
        mid_width = round(full_width * 0.22)
        right_width = round(full_width * 0.279)
        top_height = round(full_height * 0.28)
        mid_height = round(full_height * 0.21)
        bottom_height = round(full_height * 0.29)
        final_width = left_width+(board_size-2)*mid_width+right_width
        final_height = top_height+(board_size-2)*mid_height+bottom_height
        assembled_board = QPixmap(final_width, final_height)
        assembled_board.fill(Qt.transparent)
        assembled_painter = QPainter(assembled_board)
        # top left
        assembled_painter.drawPixmap(0, 0,
                                     left_width, top_height,
                                     full_board,
                                     0, 0,
                                     left_width, top_height)
        for j in range(board_size-2):
            # top middle
            assembled_painter.drawPixmap(left_width+j*mid_width, 0,
                                         mid_width, top_height,
                                         full_board,
                                         left_width, 0,
                                         mid_width, top_height)
        # top right
        assembled_painter.drawPixmap(final_width-right_width, 0,
                                     right_width, top_height,
                                     full_board,
                                     full_width-right_width, 0,
                                     right_width, top_height)
        for i in range(board_size-2):
            # left middle
            assembled_painter.drawPixmap(0, top_height+i*mid_height,
                                         left_width, mid_height,
                                         full_board,
                                         0, top_height,
                                         left_width, mid_height)
            for j in range(board_size-2):
                # middle middle
                assembled_painter.drawPixmap(
                    left_width+j*mid_width, top_height+i*mid_height,
                    mid_width, mid_height,
                    full_board,
                    left_width, top_height,
                    mid_width, mid_height)
            # right middle
            assembled_painter.drawPixmap(
                final_width-right_width, top_height+i*mid_height,
                right_width, mid_height,
                full_board,
                full_width-right_width, top_height,
                right_width, mid_height)
        # bottom left
        assembled_painter.drawPixmap(0, final_height-bottom_height,
                                     left_width, bottom_height,
                                     full_board,
                                     0, full_height - bottom_height,
                                     left_width, bottom_height)
        for j in range(board_size-2):
            # bottom middle
            assembled_painter.drawPixmap(
                left_width+j*mid_width, final_height-bottom_height,
                mid_width, bottom_height,
                full_board,
                left_width, full_height-bottom_height,
                mid_width, bottom_height)
        # bottom right
        assembled_painter.drawPixmap(
            final_width-right_width, final_height-bottom_height,
            right_width, bottom_height,
            full_board,
            full_width-right_width, full_height-bottom_height,
            right_width, bottom_height)
        return assembled_board

    def update_board(self, game_state: GameState):
        assert isinstance(game_state, ShibumiGameState)
        self.current_state = game_state
        valid_moves = game_state.get_valid_moves()
        is_ended = game_state.is_ended()
        for level, item_level in zip(game_state.get_levels(),
                                     self.item_levels):
            for row_pieces, row_items in zip(level, item_level):
                piece_item: QGraphicsPixmapItem
                for piece, piece_item in zip(row_pieces, row_items):
                    move_index = game_state.get_index(piece_item.height,
                                                      piece_item.row,
                                                      piece_item.column)
                    is_valid = valid_moves[move_index] and not is_ended
                    piece_item.setVisible(bool(piece != game_state.NO_PLAYER or
                                               is_valid))
                    if piece == game_state.WHITE:
                        piece_item.setPixmap(self.white_scaled)
                    else:
                        piece_item.setPixmap(self.black_scaled)
                    piece_item.setOpacity(0.001
                                          if piece == game_state.NO_PLAYER
                                          else 1)
        displayed_player: typing.Optional[int] = None
        if is_ended:
            if game_state.is_win(game_state.WHITE):
                self.update_move_text('wins')
                displayed_player = game_state.WHITE
            elif game_state.is_win(game_state.BLACK):
                self.update_move_text('wins')
                displayed_player = game_state.BLACK
            else:
                self.update_move_text('draw')
        else:
            displayed_player = game_state.get_active_player()
            self.update_move_text(self.choose_active_text())
        if displayed_player == game_state.WHITE:
            self.player_item.setPixmap(self.white_player)
        elif displayed_player == game_state.BLACK:
            self.player_item.setPixmap(self.black_player)
        self.player_item.setVisible(displayed_player is not None)

    def update_move_text(self, text: str = None):
        if self.debug_message:
            self.move_text.setText(self.debug_message)
        elif text is not None:
            self.move_text.setText(text)
        center_text_item(self.move_text, self.text_x, self.text_y)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        view_size = event.size()
        self.start_state: ShibumiGameState
        board_size = self.start_state.size
        if self.show_coordinates:
            # Leave room for active player and coordinates
            x_scale = 1.5
            y_scale = 1.25
        else:
            # Leave room for active player
            x_scale = 1.25
            y_scale = 1
        scaled_pixmap = self.background_pixmap.scaled(
            view_size.width() // x_scale,
            view_size.height() // y_scale,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)  # type: ignore
        self.background_item.setPixmap(scaled_pixmap)
        display_width = scaled_pixmap.width() // .795
        if self.show_coordinates:
            full_width = scaled_pixmap.width() // 0.666
            full_height = scaled_pixmap.height() // 0.8
        else:
            full_width = display_width
            full_height = scaled_pixmap.height()
        x0 = (view_size.width() - full_width) // 2
        y0 = (view_size.height() - full_height) // 2

        raw_cell_size = scaled_pixmap.width() / 4.5
        cell_size = floor(scaled_pixmap.width()/(0.541+board_size))
        raw_cell_size = floor(raw_cell_size)
        if self.show_coordinates:
            x0 += raw_cell_size
        self.background_item.setPos(x0, y0)
        ball_size = floor(cell_size * 1.154)
        self.black_scaled = self.black_pixmap.scaled(
            ball_size,
            ball_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)
        self.white_scaled = self.white_pixmap.scaled(
            ball_size,
            ball_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)
        player_size = display_width // 4.9
        self.black_player = self.black_pixmap.scaled(
            player_size,
            player_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)
        self.white_player = self.white_pixmap.scaled(
            player_size,
            player_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)
        x0 += floor(scaled_pixmap.width()*0.046/(0.119+0.22*board_size))
        y0 += floor(scaled_pixmap.height()*0.045/(0.15+0.21*board_size))
        for height, level in enumerate(self.item_levels):
            for row, row_items in enumerate(level):
                row = self.start_state.size - row - height - 1
                piece_item: QGraphicsPixmapItem
                for column, piece_item in enumerate(row_items):
                    piece_item.setPos(x0+(height + 2*column)*cell_size // 2,
                                      y0+(height + 2*row)*cell_size // 2)
        self.player_item.setPos(x0 + scaled_pixmap.width() // 1.032,
                                y0 + scaled_pixmap.height() // 3.05)
        font = QFont(self.default_font)
        font.setPointSize(raw_cell_size * 2 // 9)
        self.move_text.setFont(font)
        self.text_x = x0 + scaled_pixmap.width() + raw_cell_size // 2.3
        self.text_y = y0 + scaled_pixmap.height() // 1.65
        font.setPointSize(raw_cell_size//3.4)
        for i, label in enumerate(self.row_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(label,
                             x0 - raw_cell_size//1.25 + i % 2 * raw_cell_size//3.5,
                             y0 + raw_cell_size//1.67 + (6-i)*(raw_cell_size // 2))
        for i, label in enumerate(self.column_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(label,
                             x0 + raw_cell_size//1.65 + i*(raw_cell_size // 2),
                             y0 + full_height - raw_cell_size//1.25 - i % 2 * raw_cell_size//3.5)
        self.update_board(self.current_state)

    def on_hover_enter(self, piece_item: GraphicsShibumiPieceItem):
        assert isinstance(self.current_state, ShibumiGameState)
        levels = self.current_state.get_levels()
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        if piece != self.start_state.NO_PLAYER:
            return
        player = self.current_state.get_active_player()
        if player == self.start_state.BLACK:
            piece_item.setPixmap(self.black_scaled)
        else:
            piece_item.setPixmap(self.white_scaled)
        piece_item.setOpacity(0.5)

    def on_hover_leave(self, piece_item: GraphicsShibumiPieceItem):
        assert isinstance(self.current_state, ShibumiGameState)
        levels = self.current_state.get_levels()
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        if piece == self.start_state.NO_PLAYER:
            piece_item.setOpacity(0.001)

    def on_click(self, piece_item: GraphicsShibumiPieceItem):
        move_index = self.start_state.get_index(piece_item.height,
                                                piece_item.row,
                                                piece_item.column)
        valid_moves = self.current_state.get_valid_moves()
        if valid_moves[move_index]:
            self.make_move(move_index)

    @staticmethod
    def load_pixmap(name: str, size: QSize = None) -> QPixmap:
        file_path = ':/shibumi_images/' + name
        image = QImage(str(file_path))
        if image.isNull():
            raise ValueError(f'Unable to load image {file_path}.')
        pixmap = QPixmap(image)
        if size is not None:
            pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap
