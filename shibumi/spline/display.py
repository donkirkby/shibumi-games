from pathlib import Path

import numpy as np
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QGraphicsPixmapItem
from zero_play.game_display import GameDisplay

from shibumi.spline.game import SplineGame


class SplineDisplay(GameDisplay):
    def __init__(self):
        game = SplineGame()
        super().__init__(game)
        self.game = game
        self.background_pixmap = self.load_pixmap('board-1.png')
        self.background_item = self.scene.addPixmap(self.background_pixmap)
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
                    item = self.scene.addPixmap(self.white_scaled)
                    # item.setVisible(False)
                    item_row.append(item)
                item_level.append(item_row)
            self.item_levels.append(item_level)

    def update(self, board: np.ndarray):
        self.current_board = board

    def resize(self, view_size: QSize):
        super().resize(view_size)
        self.game: SplineGame
        scaled_pixmap = self.background_pixmap.scaled(self.scene.width(),
                                                      self.scene.height(),
                                                      Qt.KeepAspectRatio,
                                                      Qt.SmoothTransformation)
        self.background_item.setPixmap(scaled_pixmap)
        self.background_item.setPos(
            (self.scene.width() - scaled_pixmap.width()) // 2,
            (self.scene.height() - scaled_pixmap.height()) // 2)
        self.black_scaled = self.black_pixmap.scaled(self.scene.width() // 4,
                                                     self.scene.height() // 4,
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
        self.white_scaled = self.white_pixmap.scaled(self.scene.width() // 4,
                                                     self.scene.height() // 4,
                                                     Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
        cell_size = scaled_pixmap.width() // 4.5
        x0 = scaled_pixmap.width() // 21
        y0 = scaled_pixmap.height() // 22
        for height, (level, item_level) in enumerate(zip(
                self.game.get_levels(self.current_board),
                self.item_levels)):
            for row, (row_pieces, row_items) in enumerate(zip(level,
                                                              item_level)):
                row = self.game.SIZE - row - height - 1
                piece_item: QGraphicsPixmapItem
                for column, (piece, piece_item) in enumerate(zip(row_pieces,
                                                                 row_items)):
                    piece_item.setPos(x0+(height + 2*column)*cell_size // 2,
                                      y0+(height + 2*row)*cell_size // 2)
                    piece_item.setVisible(piece != self.game.NO_PLAYER)
                    if piece == self.game.WHITE:
                        piece_item.setPixmap(self.white_scaled)
                    elif piece == self.game.BLACK:
                        piece_item.setPixmap(self.black_scaled)

    @staticmethod
    def load_pixmap(name: str, size: QSize = None) -> QPixmap:
        file_path = Path(__file__).parent.parent.parent / 'images' / name
        image = QImage(str(file_path))
        if image.isNull():
            raise ValueError(f'Unable to load image {file_path}.')
        pixmap = QPixmap(image)
        if size is not None:
            pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap
