from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

def center(self):
    # Get the size of the screen
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    # Get the size of the window
    size = self.geometry()
    # Calculate the center point of the screen
    center_point = QPoint(int(screen.width() / 2), int(screen.height() / 2))
    # Calculate the top-left point of the window to center it on the screen
    top_left = center_point - QPoint(int(size.width() / 2), int(size.height() / 2))
    # Move the window to the center of the screen
    self.move(top_left)

def create_new_card(self):
    # cards QGridLayout
    cards_layout = self.cards.layout()

    # card number
    card_num = cards_layout.count() + 1

    # card
    card = QFrame()
    card.setObjectName(f'card{card_num}')
    card.setStyleSheet('QFrame#card' + str(card_num) + '{border: 1px solid black; border-radius: 10px; background-color: transparent; max-width: 280px; max-height: 140px;}')
    card_layout = QVBoxLayout(card)
    card_layout.setSpacing(0)
    card_layout.setContentsMargins(0,0,0,0)

    # card -> cardHeader
    card_header = QFrame()
    card_header.setObjectName(f'cardHeader{card_num}')
    card_header.setStyleSheet('QFrame#cardHeader' + str(card_num) + '{min-height: 40px; max-height: 40px; border-bottom: 1px solid black; border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: #2a2c33; margin-bottom: 10px;}')
    card_header_layout = QHBoxLayout(card_header)

    # cardHeader -> PC
    pc = QPushButton('  PC')
    pc.setStyleSheet('font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: white; background-color: transparent; text-align: left;')
    pc.setIcon(QIcon(':/images/resources/icons_alt/monitor.svg'))
    pc.setIconSize(QSize(20, 20))   
    card_header_layout.addWidget(pc)

    #cardHeader -> status
    status = QLabel()
    status.setObjectName(f'status{card_num}')
    status.setStyleSheet('QLabel#status' + str(card_num) + '{min-width: 6px; max-height: 6px; min-width: 6px; max-width: 6px; border-radius: 2px; background-color: green;}')
    card_header_layout.addWidget(status)

    # card-> cardContent
    card_content = QFrame()
    card_content.setObjectName(f'cardContent{card_num}')
    card_content.setStyleSheet('QFrame#cardContent' + str(card_num) + '{margin-left: 20px; margin-right: 20px;}')
    card_content_layout = QVBoxLayout(card_content)
    card_content_layout.setSpacing(0)
    card_content_layout.setContentsMargins(0,0,0,0)

    # cardContent -> cpuUsage
    cpu_usage = QFrame()
    cpu_usage.setObjectName(f'cpuUsage{card_num}')
    cpu_usage.setStyleSheet('QFrame#cpuUsage' + str(card_num) + '{margin-bottom: 10px;}')
    cpu_usage_layout = QHBoxLayout(cpu_usage)
    cpu_usage_layout.setSpacing(0)
    cpu_usage_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(cpu_usage)

    # cpuUsage -> txtCpuUsage
    txtCpuUsage = QLabel()
    txtCpuUsage.setObjectName(f'txtCpuUsage{card_num}')
    txtCpuUsage.setStyleSheet('QLabel#txtCpuUsage' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: white;}')
    txtCpuUsage.setText('CPU Usage')
    cpu_usage_layout.addWidget(txtCpuUsage)

    # cpuUsage -> cpuUsageValueText
    cpuUsageValueText = QLabel()
    cpuUsageValueText.setObjectName(f'cpuUsageValueText{card_num}')
    cpuUsageValueText.setStyleSheet('QLabel#cpuUsageValueText' + str(card_num) + '{font-family: "Segoe UI", sans-serif; color: #6a6b70;}')
    cpuUsageValueText.setText('0%')
    cpu_usage_layout.addWidget(cpuUsageValueText, alignment=QtCore.Qt.AlignRight)

    # cardContent -> cpuUsageBar
    cpu_usage_bar = QFrame()
    cpu_usage_bar.setObjectName(f'cpuUsageBar{card_num}')
    cpu_usage_bar.setStyleSheet('QFrame#cpuUsageBar' + str(card_num) + '{background-color: #262a34; border-radius: 4px; min-width: 238px; max-width: 238px; min-height: 10px; max-height: 10px;}')
    cpu_usage_bar_layout = QHBoxLayout(cpu_usage_bar)
    cpu_usage_bar_layout.setSpacing(0)
    cpu_usage_bar_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(cpu_usage_bar)

    # cpuUsageBar -> cpuUsageValue
    cpu_usage_value = QLabel()
    cpu_usage_value.setObjectName(f'cpuUsageValue{card_num}')
    cpu_usage_value.setStyleSheet('QLabel#cpuUsageValue' + str(card_num) + '{min-height: 10px; border-radius: 4px; background-color: #5468ff; min-width: 20px;}')
    cpu_usage_bar_layout.addWidget(cpu_usage_value)

    # cpuUsageBar -> horizontalSpacer
    horizontal_spacer = QSpacerItem(40,20, QSizePolicy.Expanding)
    cpu_usage_bar_layout.addSpacerItem(horizontal_spacer)

    # cardContent -> btnSeeAll
    btn_see_all = QPushButton('See all')
    btn_see_all.setObjectName(f'btnSeeAll{card_num}')
    btn_see_all.setStyleSheet('QPushButton#btnSeeAll' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: #5568fe; background-color: transparent; padding: 0px; margin-top: 10px;}')
    btn_see_all.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    card_content_layout.addWidget(btn_see_all, alignment=QtCore.Qt.AlignLeft)

    # cardContent -> vertical_spacer
    vertical_spacer = QSpacerItem(20,40, QSizePolicy.Expanding)
    card_content_layout.addSpacerItem(vertical_spacer)

    # add the widgets
    card_layout.addWidget(card_header, alignment=QtCore.Qt.AlignTop)
    card_layout.addWidget(card_content)

    # add the new card to cards
    if card_num <= 6:
        row, col = divmod(card_num - 1, 3)
        cards_layout.addWidget(card, row, col)


