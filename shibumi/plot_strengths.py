import logging
import sqlite3
from argparse import Namespace
from copy import copy
from queue import Queue, Empty
from sqlite3 import OperationalError
from threading import Thread

import numpy as np
import matplotlib.pyplot as plt
from alpha_zero_general.Arena import Arena
from matplotlib.animation import FuncAnimation
import seaborn as sn

from alpha_zero_general.pit import MCTSPlayer
from shibumi.spline.game import SplineGame

SAVED_MODEL = '../saved_models/spline4_gpu/best.pth.tar'
logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self, start_thread=True):
        self.x = 2 << np.arange(7)
        self.y = 2 << np.arange(7)
        self.x_coords, self.y_coords = np.meshgrid(self.x, self.y)
        self.counts = np.zeros(self.y_coords.shape)
        self.y_wins = np.zeros(self.y_coords.shape)
        self.result_queue = Queue()
        self.conn = sqlite3.connect('strengths.db')
        self.conn.row_factory = sqlite3.Row
        self.load_history()
        self.has_reported = False
        if start_thread:
            game_thread = Thread(target=run_games,
                                 args=(self.result_queue, self.x, self.y, self.counts.copy()),
                                 daemon=True)
            game_thread.start()
        sn.set()
        plt.ylabel('Player 1 MCTS simulation count')
        plt.xlabel('Player 2 MCTS simulation count')
        plt.xscale('log')
        plt.yscale('log')
        self.artists = []
        self.contour = None
        self.colorbar_axes = None
        self.create_contour()

    def update(self, frame):
        messages = []
        try:
            while True:
                messages.append(self.result_queue.get_nowait())
        except Empty:
            if not messages:
                return
        for x, y, result in messages:
            if result < 0:
                wins1 = 1
            else:
                wins1 = 0
            self.record_result(y, x, wins1)
        self.write_history()

        for artist in self.contour.collections:
            artist.remove()
        self.artists.clear()

        self.create_contour()
        return self.artists

    def record_result(self, strength1, strength2, wins1, count=1):
        matches = np.nonzero(self.y == strength1)
        if not matches:
            return
        i = matches[0]
        matches = np.nonzero(self.x == strength2)
        if not matches:
            return
        j = matches[0]
        self.y_wins[i, j] += wins1
        self.counts[i, j] += count

    def create_contour(self):
        z = self.y_wins / self.counts
        if not self.has_reported:
            # print(self.y_wins)
            print(self.counts)
            print(z)
            self.has_reported = True
        # np.savetxt(sys.stdout, z)
        self.contour = plt.contourf(self.x_coords, self.y_coords, z)
        self.artists.append(self.contour)
        # self.artists.append(plt.clabel(self.contour))
        self.artists.append(plt.suptitle(
            f'Player 1 Win Rates After {int(self.counts.sum())} Games'))
        self.colorbar = plt.colorbar(cax=self.colorbar_axes)
        self.artists.append(self.colorbar)
        _, self.colorbar_axes = plt.gcf().get_axes()

    def load_history(self):
        try:
            self.conn.execute("""\
CREATE
TABLE   games
        (
        strength1,
        strength2,
        count,
        wins1
        );
""")
        except OperationalError:
            # Table already exists.
            pass
        cursor = self.conn.execute("""\
SELECT  strength1,
        strength2,
        wins1,
        count
FROM    games;""")
        while True:
            rows = cursor.fetchmany()
            if not rows:
                break
            for row in rows:
                self.record_result(*row)

    def write_history(self):
        it = np.nditer(self.counts, flags=['multi_index'])
        while not it.finished:
            i, j = it.multi_index
            strength1 = int(self.y[i])
            strength2 = int(self.x[j])
            wins1 = int(self.y_wins[i, j])
            count = int(it[0])
            update_count = self.conn.execute(
                """\
UPDATE  games
SET     wins1 = ?,
        count = ?
WHERE   strength1 = ?
AND     strength2 = ?;
""",
                [wins1, count, strength1, strength2]).rowcount
            if update_count == 0:
                self.conn.execute(
                    """\
INSERT
INTO    games
        (
        strength1,
        strength2,
        count,
        wins1
        )
        VALUES
        (
        ?,
        ?,
        ?,
        ?
        )
""",
                [strength1, strength2, count, wins1])
            self.conn.commit()
            it.iternext()


def run_games(result_queue: Queue, x_values, y_values, counts):
    game = SplineGame()
    args1 = Namespace(game=game,
                      cpuct=1.0,
                      player=None,
                      load_model=SAVED_MODEL,
                      network='alpha_zero_general.connect4.tensorflow.NNet.NNetWrapper')
    args2 = copy(args1)
    player1 = MCTSPlayer(game, args1).play
    # noinspection PyUnresolvedReferences
    player2 = MCTSPlayer(game, args2).play
    arena = Arena(player1, player2, game)

    while True:
        for j, x in enumerate(x_values):
            args2.num_mcts_sims = x
            for i, y in enumerate(y_values):
                args1.num_mcts_sims = y
                # logger.debug(f'checking params {i}, {j} ({x}, {y}) with {counts[i, j]} counts')
                if counts[i, j] > counts.min():
                    continue
                counts[i, j] += 1
                result = arena.playGame()

                logger.debug(f'Result of pitting {y} vs {x}: {result}.')
                result_queue.put((x, y, result))


def main():
    start_thread = __name__ != '__live_coding__'
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s[%(levelname)s]:%(name)s:%(message)s")
    figure = plt.figure()
    plotter = Plotter(start_thread)
    animation = FuncAnimation(figure, plotter.update, interval=10000)
    plt.show()


main()

# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True, interval=0)
