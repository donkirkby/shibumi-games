from distutils.core import setup

setup(name='shibumi',
      version='0.1',
      description='Board games for the Shibumi system of stacked marbles',
      author='Don Kirkby',
      url='https://github.com/donkirkby/shibumi-games',
      packages=['shibumi'],
      scripts=['shibumi/play_shibumi.py'])
