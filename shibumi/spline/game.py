import numpy as np

from alpha_zero_general.Game import Game

from .board import Board


class SplineGame(Game):
    """
    Spline Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, size=4):
        super().__init__()
        self._base_board = Board(size)

    def getInitBoard(self):
        return self._base_board.pieces

    def getBoardSize(self):
        return self._base_board.size, self._base_board.size

    def getActionSize(self):
        return len(self._base_board.get_valid_moves())

    def getActionIndex(self, board, row, column):
        b = self._base_board.with_np_pieces(board)
        return b.get_move_index(row, column)

    def getNextState(self, board, player, action):
        """ Returns a copy of the board with updated move.

        Original board is unmodified.
        """
        b = self._base_board.with_np_pieces(np.copy(board))
        b.make_move(action, player)
        return b.pieces, -player

    def getValidMoves(self, board, player):
        return self._base_board.with_np_pieces(board).get_valid_moves()

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(board)
        winner = b.get_winner()
        if winner is None:
            if b.get_valid_moves().any():
                # 0 represents unfinished game
                return 0
            # draw has very little value.
            return 1e-4
        if winner == player:
            return +1
        if winner == -player:
            return -1
        raise ValueError('Unexpected winner found: ', winner)

    def getCanonicalForm(self, board, player):
        # Flip player from 1 to -1
        return board * player

    def getSymmetries(self, board, pi):
        """Board is left/right board symmetric"""
        return [(board, pi), (board[:, ::-1], pi)]

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))


def display(board):
    print(" -----------------------")
    b = Board(pieces=board)
    print(b)
    print(" -----------------------")
