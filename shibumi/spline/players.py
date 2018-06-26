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
