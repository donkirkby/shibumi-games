import re
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

from PySide6.QtGui import QPixmap, Qt, QPainter
from PySide6.QtWidgets import QApplication


def parse_args():
    parser = ArgumentParser(description='Launch povray command for a scene.')
    # noinspection PyTypeChecker
    parser.add_argument('pov_file',
                        type=Path,
                        help='Scene definition file')
    return parser.parse_args()


def main():
    parser = parse_args()
    pov_file: Path = parser.pov_file
    stem = pov_file.stem
    shadow_stem = re.sub(r'-(\d+)$', r'-shadow-\1', stem)
    temp_file = pov_file.parent / (stem + '-temp.png')
    temp_shadow_file = pov_file.parent / (shadow_stem + '-temp.png')
    png_file = pov_file.parent / (shadow_stem + '.png')
    current_images = Path(__file__).parent.parent / 'shibumi_images'
    current_file = current_images / png_file.name
    if current_file.exists():
        png_file = current_file
    args = ['povray',
            '-D',
            f'+I{pov_file}',
            '+V',
            '-W640',
            '-H480',
            '+ua',
            f'+O{temp_file}']
    run(args, check=True)

    app = QApplication()
    images_path = Path(__file__).parent
    shadow_file = images_path / 'ball-r-shadow-1.png'
    shadow = QPixmap(str(shadow_file))
    rendered = QPixmap(str(temp_file))
    cropped = rendered.copy(120, 20, 400, 400)
    scaled = cropped.scaled(98,
                            102,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation)

    painter = QPainter(shadow)
    try:
        painter.drawPixmap(7, 2, scaled)
    finally:
        painter.end()
    assert app

    shadow.save(str(temp_shadow_file), 'png')
    temp_file.unlink()
    temp_shadow_file.rename(png_file)
    print(f'Generated {png_file} from {pov_file}.')


main()
