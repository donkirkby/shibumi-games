from copy import copy

import numpy as np
import typing

from shibumi.shibumi_game_state import ShibumiGameState, PlayerCode


class SpookState(ShibumiGameState):
    game_name = 'Spook'
    players = (ShibumiGameState.RED, ShibumiGameState.BLACK)

    def __init__(self,
                 text: str | None = None,
                 size: int = 4):
        super().__init__(text, size=size)
        if text is None:
            active_player = self.RED
            move_line = None
        else:
            lines = text.splitlines()
            move_line = lines[-1]
            active_player = self.RED if move_line[1] == 'R' else self.BLACK
        levels = self.levels

        black_count, white_count, red_count = levels.sum(axis=(1, 2, 3))
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
        self.active_player = active_player
        self.move_count = move_count
        self.restricted_colour = restricted_colour
        # Restricted colour:
        # - UNUSABLE means we're still adding
        # - NO_PLAYER means you can remove either colour
        # - RED or BLACK means you can only remove that colour

    def display(self, show_coordinates: bool = False) -> str:
        display = super().display(show_coordinates)
        player_display = 'R' if self.active_player == self.RED else 'B'
        restricted_colour = self.restricted_colour
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
        return self.active_player

    def get_players(self) -> typing.Iterable[int]:
        return self.BLACK, self.RED

    def make_move(self, move: int) -> 'ShibumiGameState':
        player = self.get_active_player()
        volume = self.calculate_volume()
        new_player = self.BLACK if player == self.RED else self.RED
        move_count = self.get_move_count() + 1
        restricted_colour = self.restricted_colour
        if restricted_colour == self.UNUSABLE:
            # Add a piece.
            new_state = super().make_move(move)
            assert isinstance(new_state, SpookState)
            new_levels = new_state.levels
            if move_count == volume - 2:
                height = self.size - 2
                for row in range(2):
                    for column in range(2):
                        if new_levels[:, height, row, column].sum() == 0:
                            new_piece_type = self.piece_types.index(new_player)
                            new_levels[new_piece_type, height, row, column] = 1

                            # Add ghost on top
                            new_levels[1, height + 1, 0, 0] = 1

                            # No restriction on colour to remove
                            restricted_colour = self.NO_PLAYER
                            break
        elif move == volume:
            # Pass the turn.
            new_state = copy(self)
            new_levels = new_state.levels
            restricted_colour = self.NO_PLAYER
        else:
            # Remove a piece or move the ghost.
            new_state = copy(self)
            new_levels = new_state.levels
            height, row, column = move_coordinates = self.get_coordinates(move)
            removed_piece_types = np.argwhere(new_levels[:, height, row, column])
            if removed_piece_types.size:
                removed_piece_type = removed_piece_types[0, 0]
                removed_piece = self.piece_types[removed_piece_type]
            else:
                removed_piece = self.NO_PLAYER
            new_state.remove(height, row, column)
            new_levels = new_state.levels
            ghost_coordinates = new_state.find_ghost()
            restricted_colour = self.NO_PLAYER
            if ghost_coordinates != move_coordinates:
                # This wasn't a ghost drop.
                is_neighbour_captured = False
                if new_levels[:, height, row, column].sum() == 0:
                    if removed_piece == self.NO_PLAYER:
                        is_neighbour_captured = False
                    else:
                        ghost_distance = sum(abs(a-b)
                                             for a, b in zip(ghost_coordinates,
                                                             move_coordinates))
                        is_neighbour_captured = ghost_distance == 1
                    if is_neighbour_captured or removed_piece == self.NO_PLAYER:
                        # Move ghost.
                        ghost_height, ghost_row, ghost_column = ghost_coordinates
                        new_levels[:, ghost_height, ghost_row, ghost_column] = 0
                        new_levels[1, height, row, column] = 1

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
                        piece_types = np.argwhere(new_levels[:, height2, row2, column2])
                        if piece_types.size:
                            piece_type = piece_types[0, 0]
                            piece = self.piece_types[piece_type]
                        else:
                            piece = self.NO_PLAYER
                        if piece == removed_piece and self.is_free(height2,
                                                                   row2,
                                                                   column2):
                            new_player = player
                            restricted_colour = removed_piece
                            break

        new_state.levels = new_levels
        new_state.active_player = new_player
        new_state.move_count = move_count
        new_state.restricted_colour = restricted_colour
        return new_state

    def get_move_count(self) -> int:
        return self.move_count

    def get_valid_moves(self) -> np.ndarray:
        volume = self.calculate_volume(self.size)
        valid_moves = np.full(volume+1, False)
        if self.is_win(self.RED) or self.is_win(self.BLACK):
            return valid_moves

        if self.restricted_colour == self.UNUSABLE:
            # Still adding.
            self.fill_supported_moves(valid_moves)
        else:
            # If you've already moved this turn, you may pass.
            valid_moves[-1] = self.restricted_colour != self.NO_PLAYER

            # Look to see if the ghost can capture one of its neighbours.
            neighbour_count = 0
            valid_neighbour_count = 0
            levels = self.levels
            ghost_height, ghost_row, ghost_column = self.find_ghost()
            for height, row, column in self.find_possible_neighbours(
                    self.size,
                    ghost_height,
                    ghost_row,
                    ghost_column,
                    dh_start=-1,
                    dh_end=1):
                piece_types = np.argwhere(levels[:, height, row, column])
                if piece_types.size:
                    piece_type = piece_types[0, 0]
                    piece = self.piece_types[piece_type]
                else:
                    piece = self.NO_PLAYER
                if piece == self.NO_PLAYER:
                    continue
                neighbour_count += 1
                if self.restricted_colour not in (self.NO_PLAYER, piece):
                    continue
                if height == ghost_height:
                    if not self.is_free(height, row, column):
                        continue
                else:
                    if self.restricted_colour != self.NO_PLAYER:
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
                        neighbour_black, neighbour_white, neighbour_red = \
                            levels[:, height2, row2, column2]
                        if neighbour_black or neighbour_red:
                            break
                    else:
                        # No neighbours, so not allowed to move ghost there.
                        valid_moves[move] = False
            elif valid_neighbour_count == 0:
                # No free neighbours, so see which opponents can be removed.
                player = self.get_active_player()
                opponent = self.RED if player == self.BLACK else self.BLACK
                opponent_type = self.piece_types.index(opponent)
                opponent_pieces = levels[opponent_type]
                for height, row, column in np.argwhere(opponent_pieces):
                    if opponent_pieces[height, row, column]:
                        if self.is_pinned(height, row, column):
                            continue
                        move = self.get_index(height, row, column)
                        valid_moves[move] = True
        return valid_moves

    def find_ghost(self) -> typing.Tuple[int, int, int]:
        ghost_locations: np.ndarray = np.argwhere(self.levels[1])
        return tuple(ghost_locations[0])  # type: ignore

    def is_win(self, player: int) -> bool:
        if self.restricted_colour:
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
