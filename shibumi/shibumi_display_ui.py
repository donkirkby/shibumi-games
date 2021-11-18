# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shibumi_display_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

from zero_play.scaled_label import ScaledLabel
from zero_play.scaled_radio_button import ScaledRadioButton


class Ui_ShibumiDisplay(object):
    def setupUi(self, ShibumiDisplay):
        if not ShibumiDisplay.objectName():
            ShibumiDisplay.setObjectName(u"ShibumiDisplay")
        ShibumiDisplay.resize(400, 300)
        self.grid_layout = QGridLayout(ShibumiDisplay)
        self.grid_layout.setObjectName(u"grid_layout")
        self.game_display = QGraphicsView(ShibumiDisplay)
        self.game_display.setObjectName(u"game_display")

        self.grid_layout.addWidget(self.game_display, 0, 0, 8, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.grid_layout.addItem(self.verticalSpacer, 4, 1, 1, 6)

        self.move_black = ScaledRadioButton(ShibumiDisplay)
        self.move_black.setObjectName(u"move_black")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_black.sizePolicy().hasHeightForWidth())
        self.move_black.setSizePolicy(sizePolicy)
        self.move_black.setChecked(True)

        self.grid_layout.addWidget(self.move_black, 6, 1, 1, 3)

        self.white_count = ScaledLabel(ShibumiDisplay)
        self.white_count.setObjectName(u"white_count")
        sizePolicy.setHeightForWidth(self.white_count.sizePolicy().hasHeightForWidth())
        self.white_count.setSizePolicy(sizePolicy)
        self.white_count.setScaledContents(True)
        self.white_count.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.white_count, 1, 5, 1, 2)

        self.white_count_pixmap = ScaledLabel(ShibumiDisplay)
        self.white_count_pixmap.setObjectName(u"white_count_pixmap")
        sizePolicy.setHeightForWidth(self.white_count_pixmap.sizePolicy().hasHeightForWidth())
        self.white_count_pixmap.setSizePolicy(sizePolicy)
        self.white_count_pixmap.setScaledContents(True)
        self.white_count_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.white_count_pixmap, 0, 5, 1, 2)

        self.move_red = ScaledRadioButton(ShibumiDisplay)
        self.move_red.setObjectName(u"move_red")
        sizePolicy.setHeightForWidth(self.move_red.sizePolicy().hasHeightForWidth())
        self.move_red.setSizePolicy(sizePolicy)

        self.grid_layout.addWidget(self.move_red, 7, 1, 1, 3)

        self.red_count = ScaledLabel(ShibumiDisplay)
        self.red_count.setObjectName(u"red_count")
        sizePolicy.setHeightForWidth(self.red_count.sizePolicy().hasHeightForWidth())
        self.red_count.setSizePolicy(sizePolicy)
        self.red_count.setScaledContents(True)
        self.red_count.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.red_count, 1, 3, 1, 2)

        self.red_count_pixmap = ScaledLabel(ShibumiDisplay)
        self.red_count_pixmap.setObjectName(u"red_count_pixmap")
        sizePolicy.setHeightForWidth(self.red_count_pixmap.sizePolicy().hasHeightForWidth())
        self.red_count_pixmap.setSizePolicy(sizePolicy)
        self.red_count_pixmap.setScaledContents(True)
        self.red_count_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.red_count_pixmap, 0, 3, 1, 2)

        self.move_text = ScaledLabel(ShibumiDisplay)
        self.move_text.setObjectName(u"move_text")
        sizePolicy.setHeightForWidth(self.move_text.sizePolicy().hasHeightForWidth())
        self.move_text.setSizePolicy(sizePolicy)
        self.move_text.setScaledContents(True)
        self.move_text.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.move_text, 3, 1, 1, 6)

        self.black_count = ScaledLabel(ShibumiDisplay)
        self.black_count.setObjectName(u"black_count")
        sizePolicy.setHeightForWidth(self.black_count.sizePolicy().hasHeightForWidth())
        self.black_count.setSizePolicy(sizePolicy)
        self.black_count.setScaledContents(True)
        self.black_count.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.black_count, 1, 1, 1, 2)

        self.remove = ScaledRadioButton(ShibumiDisplay)
        self.remove.setObjectName(u"remove")
        sizePolicy.setHeightForWidth(self.remove.sizePolicy().hasHeightForWidth())
        self.remove.setSizePolicy(sizePolicy)

        self.grid_layout.addWidget(self.remove, 7, 4, 1, 3)

        self.move_white = ScaledRadioButton(ShibumiDisplay)
        self.move_white.setObjectName(u"move_white")
        sizePolicy.setHeightForWidth(self.move_white.sizePolicy().hasHeightForWidth())
        self.move_white.setSizePolicy(sizePolicy)

        self.grid_layout.addWidget(self.move_white, 6, 4, 1, 3)

        self.player_pixmap = ScaledLabel(ShibumiDisplay)
        self.player_pixmap.setObjectName(u"player_pixmap")
        sizePolicy.setHeightForWidth(self.player_pixmap.sizePolicy().hasHeightForWidth())
        self.player_pixmap.setSizePolicy(sizePolicy)
        self.player_pixmap.setScaledContents(True)
        self.player_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.player_pixmap, 2, 1, 1, 6)

        self.black_count_pixmap = ScaledLabel(ShibumiDisplay)
        self.black_count_pixmap.setObjectName(u"black_count_pixmap")
        sizePolicy.setHeightForWidth(self.black_count_pixmap.sizePolicy().hasHeightForWidth())
        self.black_count_pixmap.setSizePolicy(sizePolicy)
        self.black_count_pixmap.setScaledContents(True)
        self.black_count_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.black_count_pixmap, 0, 1, 1, 2)

        self.pass_button = QPushButton(ShibumiDisplay)
        self.pass_button.setObjectName(u"pass_button")

        self.grid_layout.addWidget(self.pass_button, 5, 3, 1, 2)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(2, 5)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 5)
        self.grid_layout.setRowStretch(5, 1)
        self.grid_layout.setRowStretch(6, 1)
        self.grid_layout.setRowStretch(7, 1)
        self.grid_layout.setColumnStretch(0, 30)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)
        self.grid_layout.setColumnStretch(3, 1)
        self.grid_layout.setColumnStretch(4, 1)
        self.grid_layout.setColumnStretch(5, 1)
        self.grid_layout.setColumnStretch(6, 1)

        self.retranslateUi(ShibumiDisplay)

        QMetaObject.connectSlotsByName(ShibumiDisplay)
    # setupUi

    def retranslateUi(self, ShibumiDisplay):
        ShibumiDisplay.setWindowTitle(QCoreApplication.translate("ShibumiDisplay", u"Form", None))
        self.move_black.setText(QCoreApplication.translate("ShibumiDisplay", u"B", None))
        self.white_count.setText(QCoreApplication.translate("ShibumiDisplay", u"0", None))
        self.white_count_pixmap.setText(QCoreApplication.translate("ShibumiDisplay", u"W", None))
        self.move_red.setText(QCoreApplication.translate("ShibumiDisplay", u"R", None))
        self.red_count.setText(QCoreApplication.translate("ShibumiDisplay", u"0", None))
        self.red_count_pixmap.setText(QCoreApplication.translate("ShibumiDisplay", u"R", None))
        self.move_text.setText(QCoreApplication.translate("ShibumiDisplay", u"to move", None))
        self.black_count.setText(QCoreApplication.translate("ShibumiDisplay", u"0", None))
        self.remove.setText(QCoreApplication.translate("ShibumiDisplay", u"X", None))
        self.move_white.setText(QCoreApplication.translate("ShibumiDisplay", u"W", None))
        self.player_pixmap.setText(QCoreApplication.translate("ShibumiDisplay", u"Player", None))
        self.black_count_pixmap.setText(QCoreApplication.translate("ShibumiDisplay", u"B", None))
        self.pass_button.setText(QCoreApplication.translate("ShibumiDisplay", u"Pass", None))
    # retranslateUi

