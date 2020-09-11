"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import setuptools
from setuptools import setup
from os import path
import shibumi

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='shibumi',
      version=shibumi.__version__,
      description='Simple board games hiding complexity',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://donkirkby.github.io/shibumi-games/',
      author='Don Kirkby',
      classifiers=[  # https://pypi.org/classifiers/
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Games/Entertainment :: Board Games',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8'],
      keywords='boardgames alphazero machine learning mcts shibumi',
      packages=setuptools.find_packages(),
      install_requires=['zero-play', 'numpy<1.19.0', 'PySide2'],
      extras_require={'ml': ['zero-play[ml]'],
                      'ml-gpu': ['zero-play[ml-gpu]']},
      entry_points={
          'gui_scripts': ['shibumi=shibumi.shibumi:main'],
          # The game entry point lets you add rules for new games.
          # The zero_play.game.Game class is a useful base class.
          'zero_play.game': ['spline=shibumi.spline.game:SplineGame',
                             'spargo=shibumi.spargo.game:SpargoGame'],
          # The game_display entry point lets you add screens for new games.
          # The zero_play.game_display.GameDisplay class is a useful base class.
          'zero_play.game_display': [
              'spline=shibumi.spline.display:SplineDisplay',
              'spargo=shibumi.spargo.display:SpargoDisplay']},
      project_urls={
          'Bug Reports': 'https://github.com/donkirkby/shibumi-games/issues',
          'Source': 'https://github.com/donkirkby/shibumi-games'})
