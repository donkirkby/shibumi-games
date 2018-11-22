import numpy as np


class HumanSplinePlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        while True:
            move = input()
            if len(move) != 2:
                print('Enter a row and column, like 1C.')
            else:
                row, column = move
                try:
                    action_index = self.game.getActionIndex(board, row, column)
                    return action_index
                except ValueError:
                    print('Invalid move.')


class DummyNNet:
    # noinspection PyUnusedLocal
    def __init__(self, game):
        pass

    def load_checkpoint(self,
                        folder='checkpoint',
                        filename='checkpoint.pth.tar'):
        pass

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def predict(self, board):
        return np.full(7, 1/7), np.zeros(1)
