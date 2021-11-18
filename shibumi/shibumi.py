import sys
import typing

from PySide6.QtWidgets import QApplication
from pkg_resources import EntryPoint

from zero_play.zero_play import ZeroPlayWindow


class ShibumiWindow(ZeroPlayWindow):
    icon_path = ":/shibumi_images/main_icon.png"

    @staticmethod
    def get_collection_name() -> str:
        return 'Shibumi'

    @staticmethod
    def filter_games(
            entries: typing.Iterable[EntryPoint]) -> typing.Generator[EntryPoint,
                                                                      None,
                                                                      None]:
        for entry_point in entries:
            if entry_point.module_name.startswith('shibumi.'):
                yield entry_point


def main():
    app = QApplication(sys.argv)
    window = ShibumiWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
