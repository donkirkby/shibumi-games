import sys

from PySide6.QtWidgets import QApplication

from zero_play.zero_play import ZeroPlayWindow


class ShibumiWindow(ZeroPlayWindow):
    icon_path = ":/shibumi_images/main_icon.png"

    @staticmethod
    def get_collection_name() -> str:
        return 'Shibumi'

    @staticmethod
    def filter_games(entries: list) -> list:
        shibumi_entries = [entry_point
                           for entry_point in entries
                           if entry_point.module.startswith('shibumi.')]
        return shibumi_entries


def main():
    app = QApplication(sys.argv)
    window = ShibumiWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
