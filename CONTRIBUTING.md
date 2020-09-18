# Contributing to the Shibumi Games Project
If you like this project and want to make it better, please help out. It could
be as simple as sending [@donkirkby] a nice note on Twitter, you could report a
bug, or pitch in with some development work. Check if there are some issues
labeled as [good first issues] or [help wanted].

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
[Python package index] where pip can find it. The details are at
[packaging.python.org], but the main steps are:

1. Update the version number in `shibumi/__init__.py` and development status
    in `setup.py`.
2. Activate the project's Python virtual environment.

        pipenv shell

3. Temporarily install the build tools using pip, not pipenv.

        python -m pip install --upgrade setuptools wheel twine

4. Build the release files.

        python setup.py sdist bdist_wheel

5. Upload the release to PyPI. You'll need a user name and password.

        ls dist/*
        twine upload dist/*

6. Check that the new version is on the [package page], and try installing it.

        pip install --no-cache shibumi

7. Remove the uploaded files, deactivate the virtual environment, and recreate
    it.

        rm dist/*
        exit
        pipenv clean

8. Commit the version number changes, push, and create a release on GitHub.

[packaging.python.org]: https://packaging.python.org/tutorials/packaging-projects/
[package page]: https://pypi.org/project/shibumi/


[PySide2 GUI]: https://wiki.qt.io/Qt_for_Python
[Python package index]: https://pypi.org/

## PySide2 Tools
See the Zero Play project for other useful tools in PySide2, but the main one
that is useful for working on this project is the resource compiler that
packages up the images and rules. After installing the `zero-play` library,
you can use its helper command to run the resource compiler.

    cd shibumi
    zero_play_rcc --name shibumi_rules ../docs/rules/
    zero_play_rcc ../shibumi_images/

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
