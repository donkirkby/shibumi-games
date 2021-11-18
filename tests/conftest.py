import pytest
from PySide6.QtWidgets import QApplication

from zero_play.pixmap_differ import PixmapDiffer


@pytest.fixture(scope='session')
def application():
    yield QApplication()


@pytest.fixture(scope='session')
def pixmap_differ(application):
    yield PixmapDiffer()
