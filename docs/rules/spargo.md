---
title: Spargo / Margo Rules

---

* designed by Cameron Browne
* 2 players

Spargo is a 3D extension of Go, in which pinned pieces remain active in the game
following capture. Spargo uses a 4x4 board, and Margo uses 6x6.

### Start
The board starts empty.

### Play
Players take turns adding a ball of their colour to a playable
point. The ball must have freedom (i.e. it must be visibly connected
to at least one empty board hole by a chain of visibly touching
friendly balls) following the move.

Enemy groups with no freedom are captured after each move,
except that balls supporting one or more enemy pieces are not
removed. Such balls survive capture and remain active in the
game as zombies.

Passing is not allowed.

Overpasses cut underpasses.

The superko rule applies: it is not allowed to repeat the board position of
any previous turn with the same player to move.

### End
The game ends when the current player has no legal moves,
and is won by the player with the most balls in play (counting zombies).
