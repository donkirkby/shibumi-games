### 5 Jun 2018 ###
Started the project by contacting Cameron Browne. Got permission from Néstor to
use his games. Next day, I got permission from Matt Green to use Sploof.
Got permission from Cameron to use his games and use his graphics for making a
display.

The games are all described in a [BGG list] and on [nestorgames] in the PDF
rule book.

Found a Python implementation of [Alpha Zero], along with a tutorial. Set up
this project to start work. Installed PyTorch and TensorFlow to follow the
tutorial.

[Alpha Zero]: https://github.com/suragnair/alpha-zero-general
[BGG list]: https://boardgamegeek.com/geeklist/73996/official-shibumi-games-list
[nestorgames]: https://nestorgames.com/#shibumi_detail

### 11 Jun 2018 ###
Discussed board notation with Cameron, comparing the [Akron notation] and
[Margo notation]. Margo marks all the positions on the board explicitly,
and Akron marks the first layer positions with second layer positions marked
as prime. I didn't like the clutter of doubling the markings, but I did prefer
the explicit positions over keeping the meaning of prime in your head.

My compromise was to only mark the first layer positions, but use the odd
numbers. Then refer to the second layer positions with the even numbers.
It's still explicit, but not cluttered.

    +-------------------------------+
    | \    A     C     E     G    / |
    |  +--------------___---___--+  |
    |  |             /   \_/   \ |  |
    |7 |   .     .  (   /   \   )| 7|
    |  |             \_(  B  )_/ |  |
    |  |             /  \___/  \ |  |
    |5 |   .     .  (  B  |  B  )| 5|
    |  |  ___   ___  \___/ \___/ |  |
    |  | /   \ /   \ /   \ /   \ |  |
    |3 |(     |     |  B  |  B  )| 3|
    |  | \___/ \___/ \___/ \___/ |  |
    |  | /   \ /   \ /   \ /   \ |  |
    |1 |(  B  |     |     |     )| 1|
    |  | \___/ \___/ \___/ \___/ |  |
    |  +-------------------------+  |
    | /    A     C     E     G    \ | 
    +-------------------------------+

In this example, the stacked black ball is at position 6F.

I successfully played against the 6x6 Othello opponent that comes with the
Alpha Zero General project. By "successfully", I mean that I got it to run,
not that I beat it.

I tried training the model for Connect 4 (7x6), and it finished 11 iterations
in about 20 hours. However, I haven't installed the GPU version of Tensorflow.
When I monitored the GPU with `nvidia-smi -l 1`, I saw the volatile GPU-util
bounce between 5% and 15% during self play. I didn't see any change in that
when I stopped the learning, so it was probably my video driver.

As for the result of the training: I beat it in my first two games.

[Akron notation]: http://www.gamerz.net/pbmserv/Akron/Akron.php?archive-270
[Margo notation]: http://www.gamerz.net/pbmserv/Margo/Margo.php?archive-411

### 16 Jun 2018 ###
After several hours of futzing, I got the GPU version of Tensorflow installed.
Now it finishes 11 iterations in about 3 hours: much faster!. The GPU bounces
around 50-60% while playing, and 90-100% while training.

After running 37 iterations overnight, I played against the best model, and
it was still pretty dumb. However, when I increased the MCTS iterations from
25 to 500 or 1000, it got much better! At 500, we each won when we were first
player. At 1000, it beat me when it was first player, and then beat me again
in a long game when I was first player.

Now I think I understand enough to try adding a new set of game rules.

### 21 Jun 2018 ###
Spent a few nights fighting with the setup tools, and now the Shibumi Games
project can use Alpha Zero General as a dependency. I can run Othello from
the Shibumi Games project.

Next step: implement Spline!

### 25 Jun 2018 ###
Implemented the rules of Spline, and tried playing human vs. human.

Next step: write the neural network wrapper.

### 2 Jul 2018 ###
Tried using the Connect 4 neural network wrapper without changes. I had to hack
the Shibumi `Board` to hold the pieces in an 8x8 array instead of 4x4x4.

The training session saved eight checkpoints and then quit. Only checkpoint 2
was accepted. I tried playing against the saved model, and beat it two out of
two games. It wasn't completely stupid, but it made some moves I didn't
understand.

Maybe I've messed up the symmetry or something. I have to try to understand
what the neural network code is really doing. So far, I just copied the existing
code.

It would also be nice to let the human player give board coordinates instead of
a move index.
