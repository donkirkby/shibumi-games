import linecache
import logging
import os
import sqlite3
import tracemalloc
from argparse import Namespace
from copy import copy
from pathlib import Path
from queue import Queue, Empty
from resource import getrusage, RUSAGE_SELF, getpagesize
from sqlite3 import OperationalError
from threading import Thread

import numpy as np
import matplotlib.pyplot as plt
from alpha_zero_general.Arena import Arena
from alpha_zero_general.connect4.Connect4Game import Connect4Game
from matplotlib.animation import FuncAnimation
import seaborn as sn

from alpha_zero_general.pit import MCTSPlayer

SAVED_MODEL = '../saved_models/connect4_gpu/best.pth.tar'
logger = logging.getLogger(__name__)


class Plotter:
    def __init__(self, start_thread=True):
        self.x = 2 << np.arange(4)
        self.y = 4 << np.arange(1)
        self.x_coords, self.y_coords = np.meshgrid(self.x, self.y)
        self.counts = np.zeros(self.y_coords.shape)
        self.y_wins = np.zeros(self.y_coords.shape)
        self.result_queue = Queue()
        db_path = os.path.abspath(os.path.join(__file__, '../strengths/connect4-1dummy-net.db'))
        logger.debug(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.has_reported = False
        self.game_count_history = []
        self.memory_history = []
        self.win_rate_history = []
        self.batch_size = self.batch_wins = 0
        self.load_history()
        if start_thread:
            game_thread = Thread(target=run_games,
                                 args=(self.result_queue, self.x, self.y, self.counts.copy()),
                                 daemon=True)
            game_thread.start()
        sn.set()
        if len(self.y) > 1:
            plt.ylabel('Player 1 MCTS simulation count')
            plt.yscale('log')
        else:
            plt.subplot(211)
            plt.ylabel('Neural Net Win Rate')
        plt.xlabel('MCTS Simulation Count')
        # plt.xscale('log')
        self.artists = []
        self.contour = self.line = None
        self.win_history_line = self.memory_history_line = None
        self.colorbar_axes = None
        self.create_contour()
        plt.tight_layout()

    def update(self, _frame):
        messages = []
        try:
            while True:
                messages.append(self.result_queue.get_nowait())
        except Empty:
            if not messages:
                return
        for x, y, result in messages:
            if result < -0.1:
                wins1 = 0
            elif result > 0.1:
                wins1 = 1
            else:
                wins1 = 0.5
            self.record_result(y, x, wins1)
        self.write_history()

        if self.contour is not None:
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

        if count > 1:
            # Loading historical data, don't record memory.
            return

        game_count = self.counts.sum()
        grid_size = self.counts.size
        self.batch_size += count
        self.batch_wins += wins1
        if self.batch_size >= grid_size * 50:
            self.game_count_history.append(game_count)
            win_rate = self.batch_wins / self.batch_size
            self.win_rate_history.append(win_rate)
            rss = get_resident_set_size() // 1024 // 1024
            self.memory_history.append(rss)
            logger.info('win rate %f, memory %d', win_rate, rss)
            self.batch_wins = self.batch_size = 0

    def create_contour(self):
        safe_counts = self.counts + (self.counts == 0)  # Avoid dividing by 0.
        z = self.y_wins / safe_counts
        if not self.has_reported:
            # print(self.y_wins)
            print(self.counts)
            print(z)
            self.has_reported = True
        # np.savetxt(sys.stdout, z)
        if len(self.y_coords) > 1:
            self.contour = plt.contourf(self.x_coords, self.y_coords, z)
            self.artists.append(self.contour)
            colorbar = plt.colorbar(cax=self.colorbar_axes)
            self.artists.append(colorbar)
            _, self.colorbar_axes = plt.gcf().get_axes()
        else:
            if self.line is None:
                plt.subplot(211)
                self.line, = plt.plot(self.x_coords[0], z[0])
                plt.subplot(212)
                self.win_history_line, = plt.plot(
                    self.game_count_history,
                    self.win_rate_history)
                self.win_history_line.axes.grid(False)
                plt.title('Changes Over Time')
                plt.ylabel('Player 1 Win Rate', color='C0')
                plt.xlabel('Game Count')
                plt.twinx()
                self.memory_history_line, = plt.plot(
                    self.game_count_history,
                    self.memory_history,
                    'C1')
                self.memory_history_line.axes.grid(False)
                plt.ylabel('Memory Usage (MB)', color='C1')
            else:
                self.line.set_data(self.x_coords[0], z[0])
                self.line.axes.relim()
                self.win_history_line.set_data(self.game_count_history,
                                               self.win_rate_history)
                self.memory_history_line.set_data(self.game_count_history,
                                                  self.memory_history)
                self.win_history_line.axes.relim()
                self.memory_history_line.axes.relim()
                plt.autoscale()
            self.line.axes.set_ylim(0, 1)
            self.win_history_line.axes.set_ylim(0, 1)
            self.artists.append(self.line)
            self.artists.append(self.memory_history_line)
            self.artists.append(self.win_history_line)
        self.artists.append(self.line.axes.set_title(
            f'Neural Net Strength vs MCTS in {int(self.counts.sum())} Games of Connect 4'))

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
    game = Connect4Game()
    args1 = Namespace(game=game,
                      cpuct=1.0,
                      player=None,
                      load_model=SAVED_MODEL,
                      network='alpha_zero_general.connect4.tensorflow.NNet.NNetWrapper')
    args2 = copy(args1)
    args2.network = 'shibumi.spline.players.DummyNNet'
    player1 = MCTSPlayer(game, args1).play
    # noinspection PyUnresolvedReferences
    player2 = MCTSPlayer(game, args2).play
    arena = Arena(player1, player2, game)
    game_count = 0

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
                game_count += 1
                # if game_count == 1000:
                #     tracemalloc.start()
                # elif game_count == 2000:
                #     snapshot = tracemalloc.take_snapshot()
                #     display_top(snapshot, limit=50)
                #     return


def get_resident_set_size():
    # Columns are: size resident shared text lib data dt
    statm = Path('/proc/self/statm').read_text()
    fields = statm.split()
    return int(fields[1]) * getpagesize()


def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def main():
    start_thread = __name__ != '__live_coding__'
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s[%(levelname)s]:%(name)s:%(message)s")
    figure = plt.figure()
    plotter = Plotter(start_thread)
    if not start_thread:
        plotter.write_history = lambda *args, **kwargs: None
        plotter.record_result(4, 4, 2, 4)
        plotter.record_result(4, 8, 2, 3)
        plotter.game_count_history.extend([0, 80, 120])
        plotter.win_rate_history.extend([.8, .9, .8])
        plotter.memory_history.extend(([1500, 1500, 1600]))
        plotter.result_queue.put((2, 2, -1))
        plotter.update(1)
    # noinspection PyUnusedLocal
    animation = FuncAnimation(figure, plotter.update, interval=100)
    plt.show()


main()

# ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                     init_func=init, blit=True, interval=0)
