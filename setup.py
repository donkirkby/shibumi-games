"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from os import path
import shibumi

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='shibumi',
      version=shibumi.__version__,
      description='Board games for the Shibumi system of stacked marbles',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/donkirkby/shibumi-games',
      author='Don Kirkby',
      classifiers=[  # https://pypi.org/classifiers/
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Games/Entertainment :: Board Games',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'],
      keywords='boardgames alphazero machine learning mcts shibumi',
      packages=['shibumi'],
      install_requires=['zero-play', 'numpy'],
      extras_require={'dev': ['pytest', 'coverage', 'mypy']},
      entry_points={
          # The game entry point lets you add rules for new games.
          # The zero_play.game.Game class is a useful base class.
          'zero_play.game': ['spline=shibumi.spline.game:SplineGame']},
      project_urls={
          'Bug Reports': 'https://github.com/donkirkby/shibumi-games/issues',
          'Source': 'https://github.com/donkirkby/shibumi-games'})
