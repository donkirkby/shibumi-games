---
title: Journal
subtitle: How we got here
---

## 2018
In [2018], I started the project, building on top of [Alpha Zero General], a
Python implementation of the Alpha Zero project. I got the Spline rules
implemented, but I couldn't train a neural network to be any good at it.

[2018]: 2018.md
[Alpha Zero General]: https://github.com/suragnair/alpha-zero-general

## 2019
In late 2018 and [2019], I started the [Zero Play] project as a rewrite of Alpha
Zero General that was designed to be used as a library to build other games on
top of. I also experimented with MiniGo, but couldn't figure out how to extend
it.

[2019]: 2019.md
[Zero Play]: https://donkirkby.github.io/zero-play/

## 2020
### Aug 2020
Used the new GUI feature of Zero Play to build a GUI for Spline. This made it
easy to play a bunch of games against the basic MCTS AI, and it's really hard to
beat at 600 MCTS iterations. I did manage to beat it a few times when I was the
second player, and it made surprising choices. I think when all its choices are
guaranteed to lose eventually, it will sometimes pick a move that loses
immediately. 

![First GUI for Spline]

I also converted the web site to my new favourite template: Bulma Clean Theme.

[First GUI for Spline]: 2020/first_spline_gui.png