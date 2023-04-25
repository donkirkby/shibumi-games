import typing
from math import floor

from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QFont, QResizeEvent, QPainter
from PySide6.QtWidgets import (QGraphicsPixmapItem, QGraphicsSceneHoverEvent,
                               QGraphicsSceneMouseEvent, QGraphicsScene)

from shibumi.shibumi_display_ui import Ui_ShibumiDisplay
from shibumi.shibumi_game_state import ShibumiGameState, MoveType, PlayerCode
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
        if self.hover_listener:
            self.hover_listener.on_hover_enter(self)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverLeaveEvent(event)
        if self.hover_listener:
            self.hover_listener.on_hover_leave(self)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        if self.hover_listener:
            self.hover_listener.on_click(self)
            event.accept()

    def __repr__(self):
        return (f'GraphicsShibumiPieceItem({self.height}, {self.row}, '
                f'{self.column})')


class ShibumiDisplay(GameDisplay):
    def __init__(self, start_state: ShibumiGameState):
        super().__init__(start_state)
        self.start_state = start_state

        ui = self.ui = Ui_ShibumiDisplay()
        ui.setupUi(self)
        scene = QGraphicsScene()
        ui.game_display.setScene(scene)
        self.background_pixmap = self.assemble_board()
        self.background_item = scene.addPixmap(self.background_pixmap)
        self.white_scaled = self.white_pixmap = self.load_pixmap(
            'ball-w-shadow-1.png')
        self.black_scaled = self.black_pixmap = self.load_pixmap(
            'ball-b-shadow-1.png')
        self.red_scaled = self.red_pixmap = self.load_pixmap(
            'ball-r-shadow-1.png')
        self.remove_pixmap = self.load_pixmap('ball-x-shadow-1.png')
        self.item_levels = []
        self.hovered_piece: typing.Optional[GraphicsShibumiPieceItem] = None
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
        self.ui.move_black.clicked.connect(
            lambda: self.on_move_type_selected(MoveType.BLACK))
        self.ui.move_white.clicked.connect(
            lambda: self.on_move_type_selected(MoveType.WHITE))
        self.ui.move_red.clicked.connect(
            lambda: self.on_move_type_selected(MoveType.RED))
        self.ui.remove.clicked.connect(
            lambda: self.on_move_type_selected(MoveType.REMOVE))
        self._selected_move_type = MoveType.BLACK
        self._visible_counts: typing.FrozenSet[PlayerCode] = frozenset()
        self._visible_move_types: typing.FrozenSet[MoveType] = frozenset()
        self.ui.black_count_pixmap.setText('')
        self.ui.white_count_pixmap.setText('')
        self.ui.red_count_pixmap.setText('')
        self.ui.move_black.setText('')
        self.ui.move_white.setText('')
        self.ui.move_red.setText('')
        self.ui.remove.setText('')
        self.ui.move_black.setIcon(self.black_pixmap)
        self.ui.move_white.setIcon(self.white_pixmap)
        self.ui.move_red.setIcon(self.red_pixmap)
        self.ui.remove.setIcon(self.remove_pixmap)
        self.ui.pass_button.setVisible(False)
        self.show_counts = False
        self.show_move_types = False
        self.debug_message = ''

    @property
    def visible_counts(self) -> typing.Iterable[PlayerCode]:
        return self._visible_counts

    @visible_counts.setter
    def visible_counts(self, value: typing.Iterable[PlayerCode]):
        self._visible_counts = frozenset(value)
        for code, pixmap, count_pixmap in (
                (PlayerCode.BLACK,
                 self.black_pixmap,
                 self.ui.black_count_pixmap),
                (PlayerCode.WHITE,
                 self.white_pixmap,
                 self.ui.white_count_pixmap),
                (PlayerCode.RED,
                 self.red_pixmap,
                 self.ui.red_count_pixmap)):
            if code in value:
                count_pixmap.setPixmap(pixmap)
            else:
                count_pixmap.setPixmap(QPixmap())
        self.update_count_text()

    @property
    def show_counts(self) -> bool:
        return bool(self.visible_counts)

    @show_counts.setter
    def show_counts(self, value: bool):
        if value:
            self.visible_counts = (PlayerCode.BLACK,
                                   PlayerCode.RED,
                                   PlayerCode.WHITE)
        else:
            self.visible_counts = ()

    @property
    def visible_move_types(self) -> typing.Iterable[MoveType]:
        return self._visible_move_types

    @visible_move_types.setter
    def visible_move_types(self, value: typing.Iterable[MoveType]):
        self._visible_move_types = frozenset(value)
        first_visible = None
        old_move_type = self.selected_move_type
        is_selected_visible = False
        for move_type, radio_button in ((MoveType.BLACK, self.ui.move_black),
                                        (MoveType.WHITE, self.ui.move_white),
                                        (MoveType.RED, self.ui.move_red),
                                        (MoveType.REMOVE, self.ui.remove)):
            is_visible = move_type in value
            radio_button.setVisible(is_visible)
            if is_visible:
                if first_visible is None:
                    first_visible = move_type
                if move_type == old_move_type:
                    is_selected_visible = True

        if is_selected_visible:
            self.selected_move_type = old_move_type
        elif first_visible is not None:
            self.selected_move_type = first_visible

    @property
    def show_move_types(self) -> bool:
        return bool(self.visible_move_types)

    @show_move_types.setter
    def show_move_types(self, value: bool):
        if value:
            self.visible_move_types = (MoveType.BLACK,
                                       MoveType.WHITE,
                                       MoveType.RED,
                                       MoveType.REMOVE)
        else:
            self.visible_move_types = ()

    @property
    def selected_move_type(self) -> MoveType:
        return self._selected_move_type

    @selected_move_type.setter
    def selected_move_type(self, value: MoveType):
        self._selected_move_type = value
        move_type_controls = {MoveType.WHITE: self.ui.move_white,
                              MoveType.BLACK: self.ui.move_black,
                              MoveType.RED: self.ui.move_red,
                              MoveType.REMOVE: self.ui.remove}
        move_type_controls[value].setChecked(True)

    def on_move_type_selected(self, move_type: MoveType):
        self.selected_move_type = move_type
        self.update_board(self.current_state)

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
        assembled_board.fill(Qt.GlobalColor.transparent)
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
        pixmaps = {game_state.BLACK: self.black_scaled,
                   game_state.WHITE: self.white_scaled,
                   game_state.RED: self.red_scaled,
                   game_state.NO_PLAYER: self.black_scaled}
        if self.show_move_types:
            move_type = self.selected_move_type
        else:
            move_type = MoveType.BLACK
        for level, item_level in zip(game_state.get_levels(),
                                     self.item_levels):
            for row_pieces, row_items in zip(level, item_level):
                piece_item: GraphicsShibumiPieceItem
                for piece, piece_item in zip(row_pieces, row_items):
                    move_index = game_state.get_index(piece_item.height,
                                                      piece_item.row,
                                                      piece_item.column,
                                                      move_type)
                    is_valid = valid_moves[move_index] and not is_ended
                    piece_item.setVisible(bool(piece != game_state.NO_PLAYER or
                                               is_valid))
                    piece_item.hover_listener = self if is_valid else None
                    pixmap = pixmaps[piece]
                    piece_item.setPixmap(pixmap)
                    piece_item.setOpacity(0.001
                                          if piece == game_state.NO_PLAYER
                                          else 1)
                    if piece_item == self.hovered_piece:
                        if is_valid:
                            piece_item.setOpacity(0.5)
                        else:
                            self.hovered_piece = None
        displayed_player: typing.Optional[int] = None
        if is_ended:
            if game_state.is_win(game_state.WHITE):
                self.update_move_text('wins')
                displayed_player = game_state.WHITE
            elif game_state.is_win(game_state.BLACK):
                self.update_move_text('wins')
                displayed_player = game_state.BLACK
            elif game_state.is_win(game_state.RED):
                self.update_move_text('wins')
                displayed_player = game_state.RED
            else:
                self.update_move_text('draw')
        else:
            displayed_player = game_state.get_active_player()
            self.update_move_text(self.choose_active_text())
        if displayed_player == game_state.WHITE:
            self.ui.player_pixmap.setPixmap(self.white_pixmap)
        elif displayed_player == game_state.BLACK:
            self.ui.player_pixmap.setPixmap(self.black_pixmap)
        elif displayed_player == game_state.RED:
            self.ui.player_pixmap.setPixmap(self.red_pixmap)
        if displayed_player is not None:
            displayed_player = int(displayed_player)
        self.ui.player_pixmap.setVisible(displayed_player != game_state.NO_PLAYER)
        if self.show_counts:
            self.update_count_text()

    def update_move_text(self, text: str | None = None):
        if self.debug_message:
            self.ui.move_text.setText(self.debug_message)
        elif text is not None:
            self.ui.move_text.setText(text)
    
    def scene(self) -> QGraphicsScene:
        return self.ui.game_display.scene()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        view_size = self.ui.game_display.contentsRect().size()
        self.start_state: ShibumiGameState
        board_size = self.start_state.size
        if self.show_coordinates:
            # Leave room for coordinates
            x_scale = 1.25
            y_scale = 1.25
        else:
            x_scale = 1
            y_scale = 1
        scaled_pixmap = self.scale_pixmap(self.background_pixmap,
                                          int(view_size.width() // x_scale),
                                          int(view_size.height() // y_scale))
        self.background_item.setPixmap(scaled_pixmap)
        display_width = scaled_pixmap.width()
        if self.show_coordinates:
            full_width = scaled_pixmap.width() // 0.666
            full_height = scaled_pixmap.height() // 0.8
        else:
            full_width = display_width
            full_height = scaled_pixmap.height()
        board_x = (view_size.width() - full_width) // 2
        board_y = (view_size.height() - full_height) // 2

        raw_cell_size = scaled_pixmap.width() / 4.5
        cell_size = floor(scaled_pixmap.width()/(0.541+board_size))
        raw_cell_size = floor(raw_cell_size)
        if self.show_coordinates:
            board_x += raw_cell_size
        self.background_item.setPos(board_x, board_y)
        ball_size = floor(cell_size * 1.154)
        self.black_scaled = self.scale_pixmap(self.black_pixmap,
                                              ball_size,
                                              ball_size)
        self.white_scaled = self.scale_pixmap(self.white_pixmap,
                                              ball_size,
                                              ball_size)
        self.red_scaled = self.scale_pixmap(self.red_pixmap,
                                            ball_size,
                                            ball_size)
        x0 = board_x + floor(scaled_pixmap.width()*0.046/(0.119+0.22*board_size))
        y0 = board_y + floor(scaled_pixmap.height()*0.045/(0.15+0.21*board_size))
        for height, level in enumerate(self.item_levels):
            for row, row_items in enumerate(level):
                row = self.start_state.size - row - height - 1
                piece_item: QGraphicsPixmapItem
                for column, piece_item in enumerate(row_items):
                    piece_item.setPos(x0+(height + 2*column)*cell_size // 2,
                                      y0+(height + 2*row)*cell_size // 2)
        font = QFont(self.default_font)
        font.setPointSize(raw_cell_size//3.4)
        for i, label in enumerate(self.row_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(
                label,
                board_x - raw_cell_size//1.6 + i % 2 * raw_cell_size//3.5,
                y0 + cell_size//1.7 + (self.start_state.size*2-2-i)*(cell_size // 2))
        for i, label in enumerate(self.column_labels):
            label.setVisible(self.show_coordinates)
            label.setFont(font)
            center_text_item(label,
                             x0 + cell_size//1.6 + i*(cell_size // 2),
                             board_y + full_height - raw_cell_size//1.6 -
                             i % 2 * raw_cell_size//3.5)
        self.update_board(self.current_state)
        self.scene().setSceneRect(0, 0, view_size.width(), view_size.height())

    def update_count_text(self):
        visible_counts = self.visible_counts
        for code, count in ((PlayerCode.BLACK, self.ui.black_count),
                            (PlayerCode.WHITE, self.ui.white_count),
                            (PlayerCode.RED, self.ui.red_count)):
            if code in visible_counts:
                piece_count = self.current_state.get_piece_count(code)
                count.setText(str(piece_count))
            else:
                count.setText('')

    @staticmethod
    def scale_pixmap(pixmap: QPixmap, width: int, height: int):
        scaled_pixmap = pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        return scaled_pixmap

    def on_hover_enter(self, piece_item: GraphicsShibumiPieceItem):
        assert isinstance(self.current_state, ShibumiGameState)
        if not self.can_move():
            return
        levels = self.current_state.get_levels()
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        if piece != self.start_state.NO_PLAYER:
            move_type = MoveType(piece)
        elif self.show_move_types:
            move_type = self.selected_move_type
        else:
            move_type = MoveType(self.current_state.get_active_player())
        if move_type == self.start_state.BLACK:
            piece_item.setPixmap(self.black_scaled)
        elif move_type == self.start_state.WHITE:
            piece_item.setPixmap(self.white_scaled)
        else:
            assert move_type == MoveType.RED
            piece_item.setPixmap(self.red_scaled)
        piece_item.setOpacity(0.5)
        self.hovered_piece = piece_item

    def on_hover_leave(self, piece_item: GraphicsShibumiPieceItem):
        assert isinstance(self.current_state, ShibumiGameState)
        levels = self.current_state.get_levels()
        piece = levels[piece_item.height][piece_item.row][piece_item.column]
        piece_item.setOpacity(0.001
                              if piece == self.start_state.NO_PLAYER
                              else 1.0)
        self.hovered_piece = None

    def on_click(self, piece_item: GraphicsShibumiPieceItem):
        if not self.can_move():
            return
        move_index = self.start_state.get_index(piece_item.height,
                                                piece_item.row,
                                                piece_item.column,
                                                self.selected_move_type)
        valid_moves = self.current_state.get_valid_moves()
        if valid_moves[move_index]:
            self.make_move(move_index)

    @staticmethod
    def load_pixmap(name: str, size: QSize | None = None) -> QPixmap:
        file_path = ':/shibumi_images/' + name
        image = QImage(str(file_path))
        if image.isNull():
            raise ValueError(f'Unable to load image {file_path}.')
        pixmap = QPixmap(image)
        if size is not None:
            pixmap = ShibumiDisplay.scale_pixmap(pixmap,
                                                 size.width(),
                                                 size.height())
        return pixmap

    def close(self):
        super().close()
        self.scene().clear()
