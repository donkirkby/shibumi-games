import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, PlayerCode


class SpookState(ShibumiGameState):
    game_name = 'Spook'
    players = (ShibumiGameState.RED, ShibumiGameState.BLACK)

    def __init__(self,
                 text: str | None = None,
                 board: np.ndarray | None = None,
                 size: int = 4):
        super().__init__(text, board, size)
        if board is None:
            if text is None:
                active_player = self.RED
                move_line = None
            else:
                lines = text.splitlines()
                move_line = lines[-1]
                active_player = self.RED if move_line[1] == 'R' else self.BLACK
            spaces = self.board.reshape(self.size*self.size*self.size)[:-3]
            # noinspection PyUnresolvedReferences
            black_count = (spaces == self.BLACK).sum()
            # noinspection PyUnresolvedReferences
            red_count = (spaces == self.RED).sum()
            # noinspection PyUnresolvedReferences
            white_count = (spaces == self.WHITE).sum()
            if white_count == 0:
                move_count = black_count + red_count
                restricted_colour = self.UNUSABLE
            else:
                assert move_line is not None
                volume = self.calculate_volume()
                move_count = 2*volume - black_count - red_count - 3
                restriction = move_line[3:-1]
                if restriction == 'B':
                    restricted_colour = self.BLACK
                elif restriction == 'R':
                    restricted_colour = self.RED
                else:
                    restricted_colour = self.NO_PLAYER

            # Extras, reversed: active player, move count, restricted colour
            self.board[-1, -1, -1] = active_player
            self.board[-1, -1, -2] = move_count
            self.board[-1, -1, -3] = restricted_colour
            # Restricted colour:
            # - UNUSABLE means we're still adding
            # - NO_PLAYER means you can remove either colour
            # - RED or BLACK means you can only remove that colour

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player_display = 'R' if self.get_active_player() == self.RED else 'B'
        restricted_colour = self.board[-1, -1, -3]
        if restricted_colour == self.UNUSABLE:
            allowed_display = ''
        elif restricted_colour == self.NO_PLAYER:
            allowed_display = '(B,R)'
        else:
            colour_name = PlayerCode(restricted_colour).name[0]
            allowed_display = f'({colour_name})'

        display += f'>{player_display}{allowed_display}\n'
        return display

    def get_active_player(self) -> int:
        return self.board[-1, -1, -1]

    def get_players(self) -> typing.Iterable[int]:
        return self.BLACK, self.RED

    def make_move(self, move: int) -> 'ShibumiGameState':
        player = self.get_active_player()
        volume = self.calculate_volume()
        new_player = self.BLACK if player == self.RED else self.RED
        move_count = self.get_move_count() + 1
        restricted_colour = self.board[-1, -1, -3]
        if restricted_colour == self.UNUSABLE:
            # Add a piece.
            new_state = super().make_move(move)
            new_board = new_state.board
            if move_count == volume - 2:
                height = self.size - 2
                for row in range(2):
                    for column in range(2):
                        if new_board[height, row, column] == self.NO_PLAYER:
                            new_board[height, row, column] = new_player

                            # Add ghost on top
                            new_board[height+1, 0, 0] = self.WHITE

                            # No restriction on colour to remove
                            restricted_colour = self.NO_PLAYER
                            break
        elif move == volume:
            # Pass the turn.
            new_state = self.__class__(board=self.board.copy())
            new_board = new_state.board
            restricted_colour = self.NO_PLAYER
        else:
            # Remove a piece or move the ghost.
            new_state = self.__class__(board=self.board.copy())
            new_board = new_state.board
            move_coordinates = self.get_coordinates(move)
            removed_piece = new_board[move_coordinates]
            new_state.remove(*move_coordinates)
            ghost_coordinates = new_state.find_ghost()
            restricted_colour = self.NO_PLAYER
            if ghost_coordinates != move_coordinates:
                # This wasn't a ghost drop.
                is_neighbour_captured = False
                if new_board[move_coordinates] == self.NO_PLAYER:
                    if removed_piece == self.NO_PLAYER:
                        is_neighbour_captured = False
                    else:
                        ghost_distance = sum(abs(a-b)
                                             for a, b in zip(ghost_coordinates,
                                                             move_coordinates))
                        is_neighbour_captured = ghost_distance == 1
                    if is_neighbour_captured or removed_piece == self.NO_PLAYER:
                        # Move ghost.
                        new_board[ghost_coordinates] = self.NO_PLAYER
                        new_board[move_coordinates] = self.WHITE

                if is_neighbour_captured:
                    # Check if more matching neighbours are available.
                    height, row, column = move_coordinates
                    for height2, row2, column2 in self.find_possible_neighbours(
                            self.size,
                            height,
                            row,
                            column,
                            dh_start=0,
                            dh_end=1):
                        piece = new_board[height2, row2, column2]
                        if piece == removed_piece and self.is_free(height2,
                                                                   row2,
                                                                   column2):
                            new_player = player
                            restricted_colour = removed_piece
                            break

        new_board[-1, -1, -1] = new_player
        new_board[-1, -1, -2] = move_count
        new_board[-1, -1, -3] = restricted_colour
        return new_state

    def get_move_count(self) -> int:
        return int(self.board[-1, -1, -2])

    def get_valid_moves(self) -> np.ndarray:
        volume = self.calculate_volume(self.size)
        valid_moves = np.full(volume+1, False)
        if self.is_win(self.RED) or self.is_win(self.BLACK):
            return valid_moves

        restricted_colour = self.board[-1, -1, -3]
        if restricted_colour == self.UNUSABLE:
            # Still adding.
            self.fill_supported_moves(valid_moves)
        else:
            # If you've already moved this turn, you may pass.
            valid_moves[-1] = restricted_colour != self.NO_PLAYER

            # Look to see if the ghost can capture one of its neighbours.
            neighbour_count = 0
            valid_neighbour_count = 0
            ghost_height, ghost_row, ghost_column = self.find_ghost()
            for height, row, column in self.find_possible_neighbours(
                    self.size,
                    ghost_height,
                    ghost_row,
                    ghost_column,
                    dh_start=-1,
                    dh_end=1):
                piece = self.board[height, row, column]
                if piece == self.NO_PLAYER:
                    continue
                neighbour_count += 1
                if restricted_colour not in (self.NO_PLAYER, piece):
                    continue
                if height == ghost_height:
                    if not self.is_free(height, row, column):
                        continue
                else:
                    if restricted_colour != self.NO_PLAYER:
                        # Can't drop once you start moving horizontally.
                        continue
                    if self.is_pinned(height, row, column):
                        continue
                move = self.get_index(height, row, column)
                valid_moves[move] = True
                valid_neighbour_count += 1
            if neighbour_count == 0:
                # No neighbours, so see where the ghost can move.
                self.fill_supported_moves(valid_moves)
                for move, in np.argwhere(valid_moves):
                    height, row, column = self.get_coordinates(move)
                    if height > 0:
                        # Any valid moves are supported, so stop checking.
                        break
                    for height2, row2, column2 in self.find_possible_neighbours(
                            self.size,
                            height,
                            row,
                            column,
                            dh_start=0,
                            dh_end=1):
                        neighbour_piece = self.board[height2, row2, column2]
                        if neighbour_piece not in (self.WHITE, self.NO_PLAYER):
                            break
                    else:
                        # No neighbours, so not allowed to move ghost there.
                        valid_moves[move] = False
            elif valid_neighbour_count == 0:
                # No free neighbours, so see which opponents can be removed.
                player = self.get_active_player()
                opponent = self.RED if player == self.BLACK else self.BLACK
                opponent_pieces = self.board == opponent
                for height, row, column in np.argwhere(opponent_pieces):
                    piece = self.board[height, row, column]
                    if piece == opponent:
                        if self.is_pinned(height, row, column):
                            continue
                        move = self.get_index(height, row, column)
                        valid_moves[move] = True
        return valid_moves

    def find_ghost(self) -> typing.Tuple[int, int, int]:
        ghost_locations: np.ndarray = np.argwhere(self.board == self.WHITE)
        return tuple(ghost_locations[0])  # type: ignore

    def is_win(self, player: int) -> bool:
        if self.board[-1, -1, -3] == self.UNUSABLE:
            return False
        pieces = self.get_piece_count(player)
        return pieces == 0

    def get_winner(self) -> int:
        """ Decide which player has won, if any.

        :return: the player number of the winner, or NO_PLAYER if neither has
            won.
        """
        for player in self.players:
            if self.is_win(player):
                return player

        return self.NO_PLAYER

    def display_move(self, move: int) -> str:
        if move == self.calculate_volume():
            return 'PASS'
        return super().display_move(move)
