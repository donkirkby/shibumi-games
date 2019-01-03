""" Simulate a simple game where two players flip coins, and the most heads wins.

Plot the win rates as each player flips a different number of coins. This was
meant to show how I expected the MCTS players' strengths to vary with the
number of iterations.
"""

from random import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn


counts = 2 << np.arange(7)
x_coords, y_coords = np.meshgrid(counts, counts)
z = np.zeros(x_coords.shape)
trial_count = 100
for i, y in enumerate(counts):
    for j, x in enumerate(counts):
        y_wins = 0.0
        for _ in range(trial_count):
            a = random()
            x_total = sum(random() for _ in range(x))
            y_total = sum(random() for _ in range(y))
            if x_total < y_total:
                y_wins += 1
            elif x_total == y_total:
                y_wins += 0.5
        z[i][j] = (y_wins / trial_count)
sn.set()
plt.contourf(x_coords, y_coords, z)
plt.colorbar()
plt.ylabel('Player 1 Flips')
plt.xlabel('Player 2 Flips')
plt.xscale('log')
plt.yscale('log')
game_count = trial_count*len(counts)*len(counts)
plt.title(f'Player 1 Win Rate After {game_count} Games of Headcount')
plt.tight_layout()
plt.show()
