import numpy as np
import typing
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap, QFont, QResizeEvent
from PySide2.QtWidgets import (QGraphicsPixmapItem, QGraphicsSceneHoverEvent,
                               QGraphicsSceneMouseEvent)

from shibumi.shibumi_game import ShibumiGame
from zero_play.game_display import GameDisplay, center_text_item

# noinspection PyUnresolvedReferences
from shibumi import shibumi_images_rc


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
    def __init__(self, game: ShibumiGame):
        super().__init__(game)
        self.game = game
        self.background_pixmap = self.load_pixmap('board-1.png')
        scene = self.scene()
        self.background_item = scene.addPixmap(self.background_pixmap)
        self.white_scaled = self.white_pixmap = self.load_pixmap(
            'ball-w-shadow-1.png')
        self.black_scaled = self.black_pixmap = self.load_pixmap(
            'ball-b-shadow-1.png')
        self.item_levels = []
        for height in range(self.game.SIZE):
            item_level = []
            for row in range(self.game.SIZE - height):
                item_row = []
                for column in range(self.game.SIZE - height):
                    item = GraphicsShibumiPieceItem(height, row, column, self)
                    scene.addItem(item)
                    item_row.append(item)
                item_level.append(item_row)
            self.item_levels.append(item_level)
        self.row_labels = []
        self.column_labels = []
        for i in range(self.game.SIZE*2-1):
            self.row_labels.append(scene.addSimpleText(str(i + 1)))
            self.column_labels.append(scene.addSimpleText(chr(i + 65)))
        self.player_item = scene.addPixmap(QPixmap())
        self.move_text = scene.addSimpleText('')
        self.text_x = self.text_y = 0
        self.debug_message = ''

    def update_board(self, board: np.ndarray):
        self.current_board = board
        valid_moves = self.game.get_valid_moves(board)
        is_ended = self.game.is_ended(board)
        for level, item_level in zip(self.game.get_levels(self.current_board),
                                     self.item_levels):
            for row_pieces, row_items in zip(level, item_level):
                piece_item: QGraphicsPixmapItem
                for piece, piece_item in zip(row_pieces, row_items):
                    move_index = self.game.get_index(piece_item.height,
                                                     piece_item.row,
                                                     piece_item.column)
                    is_valid = valid_moves[move_index] and not is_ended
                    piece_item.setVisible(bool(piece != self.game.NO_PLAYER or
                                               is_valid))
                    if piece == self.game.WHITE:
                        piece_item.setPixmap(self.white_scaled)
                    else:
                        piece_item.setPixmap(self.black_scaled)
                    piece_item.setOpacity(0.001
                                          if piece == self.game.NO_PLAYER
                                          else 1)
        displayed_player: typing.Optional[int] = None
        if is_ended:
            if self.game.is_win(board, self.game.WHITE):
                self.update_move_text('wins')
                displayed_player = self.game.WHITE
            elif self.game.is_win(board, self.game.BLACK):
                self.update_move_text('wins')
                displayed_player = self.game.BLACK
            else:
                self.update_move_text('draw')
        else:
            displayed_player = self.game.get_active_player(board)
            self.update_move_text(self.choose_active_text())
        if displayed_player == self.game.WHITE:
            self.player_item.setPixmap(self.white_scaled)
        elif displayed_player == self.game.BLACK:
            self.player_item.setPixmap(self.black_scaled)
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
        self.game: ShibumiGame
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
        cell_size = scaled_pixmap.width() // 4.5
        if self.show_coordinates:
            x0 += cell_size
        self.background_item.setPos(x0, y0)
        self.black_scaled = self.black_pixmap.scaled(display_width // 4.9,
                                                     display_width // 4.9,
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
        self.white_scaled = self.white_pixmap.scaled(display_width // 4.9,
                                                     display_width // 4.9,
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
        x0 += scaled_pixmap.width() // 22
        y0 += scaled_pixmap.height() // 22
        for height, level in enumerate(self.item_levels):
            for row, row_items in enumerate(level):
                row = self.game.SIZE - row - height - 1
                piece_item: QGraphicsPixmapItem
                for column, piece_item in enumerate(row_items):
                    piece_item.setPos(x0+(height + 2*column)*cell_size // 2,
                                      y0+(height + 2*row)*cell_size // 2)
        self.player_item.setPos(x0 + scaled_pixmap.width() // 1.032,
                                y0 + scaled_pixmap.height() // 3.05)
        font = QFont(self.default_font)
        font.setPointSize(cell_size * 2 // 9)
        self.move_text.setFont(font)
        self.text_x = x0 + scaled_pixmap.width() + cell_size // 2.3
        self.text_y = y0 + scaled_pixmap.height() // 1.65
        font.setPointSize(cell_size//3.4)
        for i, label in enumerate(self.row_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(label,
                             x0 - cell_size//1.25 + i % 2 * cell_size//3.5,
                             y0 + cell_size//1.67 + (6-i)*(cell_size // 2))
        for i, label in enumerate(self.column_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(label,
                             x0 + cell_size//1.65 + i*(cell_size // 2),
                             y0 + full_height - cell_size//1.25 - i % 2 * cell_size//3.5)
        self.update_board(self.current_board)

    def on_hover_enter(self, piece_item: GraphicsShibumiPieceItem):
        levels = self.game.get_levels(self.current_board)
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        if piece != self.game.NO_PLAYER:
            return
        player = self.game.get_active_player(self.current_board)
        if player == self.game.BLACK:
            piece_item.setPixmap(self.black_scaled)
        else:
            piece_item.setPixmap(self.white_scaled)
        piece_item.setOpacity(0.5)

    def on_hover_leave(self, piece_item: GraphicsShibumiPieceItem):
        levels = self.game.get_levels(self.current_board)
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        if piece == self.game.NO_PLAYER:
            piece_item.setOpacity(0.001)

    def on_click(self, piece_item: GraphicsShibumiPieceItem):
        move_index = self.game.get_index(piece_item.height,
                                         piece_item.row,
                                         piece_item.column)
        valid_moves = self.game.get_valid_moves(self.current_board)
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
