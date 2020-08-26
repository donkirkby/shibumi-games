# Contributing to the Shibumi Games Project
If you like this project and want to make it better, help out. It could be as
simple as sending [@donkirkby] a nice note on Twitter, you could report a bug,
or pitch in with some development work. Check if there are some issues labeled
as [good first issues] or [help wanted].

[@donkirkby]: https://twitter.com/donkirkby
[good first issues]: https://github.com/donkirkby/shibumi-games/labels/good%20first%20issue
[help wanted]: https://github.com/donkirkby/shibumi-games/labels/help%20wanted

## Bug Reports and Enhancement Requests
Please create issue descriptions [on GitHub][issues]. Be as specific as possible.
Which version are you using? What did you do? What did you expect to happen? Are
you planning to submit your own fix in a pull request? Please include a game
transcript if that helps explain the problem.

[issues]: https://github.com/donkirkby/shibumi-games/issues?state=open

## Building a Release
The nice thing about using the [PySide2 GUI] is that users can install Shibumi
Games with pip. Releasing a new version means publishing it on the
[Python package index] where pip can find it.

[PySide2 GUI]: https://wiki.qt.io/Qt_for_Python
[Python package index]: https://pypi.org/

## PySide2 Tools
See the Zero Play project for other useful tools in PySide2, but the main one
that is useful for working on this project is the resource compiler that
packages up the images into `shibumi_images_rc.py`

You can update the `images.qrc` file by hand, or you can generate it:

    cd shibumi_images
    pyside2-rcc --project > shibumi_images.qrc
    cd ..

After changing the `images.qrc` file or the image files, recompile the resource
file. Run this from the project's root folder:

    pyside2-rcc -o shibumi/shibumi_images_rc.py --root /shibumi_images shibumi_images/shibumi_images.qrc

## Testing GitHub Pages locally
The web site uses the [Bulma Clean theme], which is based on [Bulma]. The
[Bulma colours] can be particularly helpful to learn about.

GitHub generates all the web pages from markdown files, but it can be useful to
test out that process before you commit changes. See the detailed instructions
for setting up [Jekyll], but the main command is this:

    cd docs
    bundle exec jekyll serve

[Bulma Clean theme]: https://github.com/chrisrhymes/bulma-clean-theme
[Bulma]: https://bulma.io/documentation/
[Bulma colours]: https://bulma.io/documentation/overview/colors/
[Jekyll]: https://help.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll
