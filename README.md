# Shibumi Games [![Build Badge]][build] [![Coverage Badge]][codecov] [![PyPI Badge]][pypi]
### Simple board games hiding complexity

[Build Badge]: https://github.com/donkirkby/shibumi-games/actions/workflows/py-build.yml/badge.svg?branch=master
[build]: https://github.com/donkirkby/shibumi-games/actions
[Coverage Badge]: https://codecov.io/github/donkirkby/shibumi-games/coverage.svg?branch=master
[codecov]: https://codecov.io/github/donkirkby/shibumi-games?branch=master
[PyPI Badge]: https://badge.fury.io/py/shibumi.svg
[pypi]: https://badge.fury.io/py/shibumi
[screenshot]: https://donkirkby.github.io/shibumi-games/images/demo.png
[journal]: https://donkirkby.github.io/shibumi-games/journal

Play board games that use the [Shibumi] game system of marbles stacked on a 4x4
board, build computer opponents for those games, learn strategy, and analyse the
structure of the games.

![screenshot]

## Installing Shibumi Games
Even though Shibumi Games has a graphical display, it is a regular Python package,
so you can install it with `pip install shibumi`. If you haven't installed
Python packages before, read Brett Cannon's [quick-and-dirty guide].

Then run it with the `shibumi` command.

The default installation generates some errors about `bdist_wheel` that don't
seem to actually cause any problems. You can either ignore them, or install
`wheel` before installing Shibumi Games.

    pip install wheel
    pip install shibumi
    shibumi

Known bug on Ubuntu 20.04:

> qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though
> it was found.

This is a [PySide2 bug] that is missing some dependencies. You can work around
it by installing those dependencies like this:

    sudo apt install libxcb-xinerama0

[quick-and-dirty guide]: https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/
[PySide2 bug]: https://bugreports.qt.io/browse/QTBUG-84749

### Game Credits
The Shibumi game system was designed by Cameron Browne and Néstor Romeral
Andrés. The complete set of game rules are available on the
[nestorgames web site], and the games used in this project are used with the
generous permission of the designers. There are more games in a [BGG list].
* Spaiji was designed by Néstor Romeral Andrés.
* Spargo and Margo were designed by Cameron Browne.
* Spire was designed by Dieter Stein, and took second place in the Shibumi
Challenge.
* Spline was designed by Néstor Romeral Andrés.
* Sploof was designed by Matt Green, and took first place in the Shibumi
Challenge.
* Spook was designed by Dieter Stein.

[nestorgames web site]: https://nestorgames.com/shibumibook_detail.html
[BGG list]: https://boardgamegeek.com/boardgamefamily/13434/series-shibumi/linkeditems/boardgamefamily?pageid=1&sort=usersrated

### Image Credits
The marble and board graphics were designed by Cameron Browne, and are used with
permission.

Some of the buttons combine Cameron's POV-Ray graphics with icons from the
[Open Iconic] project.

[Open Iconic]: https://useiconic.com/open

## More Information
If you'd like to help out with the project, or add your own games, see the
`CONTRIBUTING.md` file in the source code. For all the details, look through the
design [journal] for the project.

Shibumi games are built on top of the [Zero Play library] that you can use to
build your own games.

[Shibumi]: https://boardgamegeek.com/boardgame/135270/shibumi
[Zero Play library]: https://donkirkby.github.io/zero-play/
