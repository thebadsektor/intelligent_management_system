from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSizeGrip

class CustomWindow(QMainWindow):
    def closeEvent(self, event):
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.mouse_pos:
            delta = QPoint(event.globalPos() - self.mouse_pos)
            self.move(self.pos() + delta)
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mouse_pos = None
        event.accept()

    def resizeEvent(self, event):
        size_grip = self.findChild(QSizeGrip)
        size_grip.setGeometry(self.rect().right() - 20, self.rect().bottom() - 20, 20, 20)
        super().resizeEvent(event)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
            self.btnMaximize.setStyleSheet("QPushButton#btnMaximize {image: url(:/images/resources/icons/square_alt.svg); min-width: 15px; max-width: 15px; padding-left: 20px; padding-right: 20px; min-height: 45px; max-height: 45px; background-color: transparent; border: 0px;} QPushButton#btnMaximize:hover {background-color: #3d4145;}")
        else:
            self.showMaximized()
            self.btnMaximize.setStyleSheet("QPushButton#btnMaximize {image: url(:/images/resources/icons_alt/copy.svg); min-width: 16px; max-width: 16px; padding-left: 20px; padding-right: 20px; min-height: 45px; max-height: 45px; background-color: transparent; border: 0px;} QPushButton#btnMaximize:hover {background-color: #3d4145;}")


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
    card.setStyleSheet('QFrame#card' + str(card_num) + '{border: 1px solid black; border-radius: 10px; background-color: transparent; max-width: 280px; max-height: 255px;}')
    card_layout = QVBoxLayout(card)
    card_layout.setSpacing(0)
    card_layout.setContentsMargins(0,0,0,0)

    # card -> cardHeader
    card_header = QFrame()
    card_header.setObjectName(f'cardHeader{card_num}')
    card_header.setStyleSheet('QFrame#cardHeader' + str(card_num) + '{min-height: 40px; max-height: 40px; border-bottom: 1px solid black; border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: #26272D;}')
    card_header_layout = QHBoxLayout(card_header)
    card_header_layout.setSpacing(0)
    card_header_layout.setContentsMargins(0,0,0,0)

    # cardHeader -> PC
    pc = QPushButton('')
    pc.setObjectName(f'pc{card_num}')
    pc.setStyleSheet('font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: white; background-color: transparent; text-align: left; margin-left: 15px;')
    pc.setIcon(QIcon(':/images/resources/icons_alt/monitor.svg'))
    pc.setIconSize(QSize(20, 20))   
    card_header_layout.addWidget(pc)

    #cardHeader -> status
    status = QLabel()
    status.setObjectName(f'status{card_num}')
    status.setStyleSheet('QLabel#status' + str(card_num) + '{min-width: 6px; max-height: 6px; min-width: 6px; max-width: 6px; border-radius: 2px; background-color: #28A745; margin-right: 15px;}')
    card_header_layout.addWidget(status)

    # card-> cardContent
    card_content = QFrame()
    card_content.setObjectName(f'cardContent{card_num}')
    card_content.setStyleSheet('QFrame#cardContent' + str(card_num) + '{padding: 15px; background-color: transparent;}')
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
    cpu_usage_bar.setStyleSheet('QFrame#cpuUsageBar' + str(card_num) + '{background-color: #26272D; border-radius: 4px; min-width: 248px; max-width: 248px; min-height: 10px; max-height: 10px;}')
    cpu_usage_bar_layout = QHBoxLayout(cpu_usage_bar)
    cpu_usage_bar_layout.setSpacing(0)
    cpu_usage_bar_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(cpu_usage_bar)

    # cpuUsageBar -> cpuUsageValue
    cpu_usage_value = QLabel()
    cpu_usage_value.setObjectName(f'cpuUsageValue{card_num}')
    cpu_usage_value.setStyleSheet('QLabel#cpuUsageValue' + str(card_num) + '{min-height: 10px; border-radius: 4px; background-color: #5468ff; min-width: 0px;}')
    cpu_usage_bar_layout.addWidget(cpu_usage_value)

    # cpuUsageBar -> horizontalSpacer
    cpu_usage_bar_layout.addSpacerItem(QSpacerItem(40,20, QSizePolicy.Expanding))

    #### begin::Memory Usage ####

    # cardContent -> memoryUsage
    memory_usage = QFrame()
    memory_usage.setObjectName(f'memoryUsage{card_num}')
    memory_usage.setStyleSheet('QFrame#memoryUsage' + str(card_num) + '{margin-top: 10px; margin-bottom: 10px;}')
    memory_usage_layout = QHBoxLayout(memory_usage)
    memory_usage_layout.setSpacing(0)
    memory_usage_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(memory_usage)

    # memoryUsage -> memoryUsageLabel
    memoryUsageLabel = QLabel()
    memoryUsageLabel.setObjectName(f'memoryUsageLabel{card_num}')
    memoryUsageLabel.setStyleSheet('QLabel#memoryUsageLabel' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: white;}')
    memoryUsageLabel.setText('Memory Usage')
    memory_usage_layout.addWidget(memoryUsageLabel)

    # memoryUsage -> memoryUsageText
    memoryUsageText = QLabel()
    memoryUsageText.setObjectName(f'memoryUsageText{card_num}')
    memoryUsageText.setStyleSheet('QLabel#memoryUsageText' + str(card_num) + '{font-family: "Segoe UI", sans-serif; color: #6a6b70;}')
    memoryUsageText.setText('0 GB / 0 GB')
    memory_usage_layout.addWidget(memoryUsageText, alignment=QtCore.Qt.AlignRight)

    # cardContent -> memoryUsageBar
    memory_usage_bar = QFrame()
    memory_usage_bar.setObjectName(f'memoryUsageBar{card_num}')
    memory_usage_bar.setStyleSheet('QFrame#memoryUsageBar' + str(card_num) + '{background-color: #26272D; border-radius: 4px; min-width: 248px; max-width: 248px; min-height: 10px; max-height: 10px;}')
    memory_usage_bar_layout = QHBoxLayout(memory_usage_bar)
    memory_usage_bar_layout.setSpacing(0)
    memory_usage_bar_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(memory_usage_bar)

    # memoryUsageBar -> memoryUsageBarValue
    memory_usage_bar_value = QLabel()
    memory_usage_bar_value.setObjectName(f'memoryUsageBarValue{card_num}')
    memory_usage_bar_value.setStyleSheet('QLabel#memoryUsageBarValue' + str(card_num) + '{min-height: 10px; border-radius: 4px; background-color: #5468ff; min-width: 0px;}')
    memory_usage_bar_layout.addWidget(memory_usage_bar_value)

    # memoryUsageBar -> horizontalSpacer
    memory_usage_bar_layout.addSpacerItem(QSpacerItem(40,20, QSizePolicy.Expanding))

    #### end::Memory Usage ####


    #### begin::Disk Usage ####

    # cardContent -> memoryUsage
    disk_usage = QFrame()
    disk_usage.setObjectName(f'diskUsage{card_num}')
    disk_usage.setStyleSheet('QFrame#diskUsage' + str(card_num) + '{margin-top: 10px; margin-bottom: 10px;}')
    disk_usage_layout = QHBoxLayout(disk_usage)
    disk_usage_layout.setSpacing(0)
    disk_usage_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(disk_usage)

    # diskUsage -> diskUsageLabel
    diskUsageLabel = QLabel()
    diskUsageLabel.setObjectName(f'diskUsageLabel{card_num}')
    diskUsageLabel.setStyleSheet('QLabel#diskUsageLabel' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: white;}')
    diskUsageLabel.setText('Disk Usage')
    disk_usage_layout.addWidget(diskUsageLabel)

    # diskUsage -> diskUsageText
    diskUsageText = QLabel()
    diskUsageText.setObjectName(f'diskUsageText{card_num}')
    diskUsageText.setStyleSheet('QLabel#diskUsageText' + str(card_num) + '{font-family: "Segoe UI", sans-serif; color: #6a6b70;}')
    diskUsageText.setText('0 GB / 0 GB')
    disk_usage_layout.addWidget(diskUsageText, alignment=QtCore.Qt.AlignRight)

    # cardContent -> diskUsageBar
    disk_usage_bar = QFrame()
    disk_usage_bar.setObjectName(f'diskUsageBar{card_num}')
    disk_usage_bar.setStyleSheet('QFrame#diskUsageBar' + str(card_num) + '{background-color: #26272D; border-radius: 4px; min-width: 248px; max-width: 248px; min-height: 10px; max-height: 10px;}')
    disk_usage_bar_layout = QHBoxLayout(disk_usage_bar)
    disk_usage_bar_layout.setSpacing(0)
    disk_usage_bar_layout.setContentsMargins(0,0,0,0)
    card_content_layout.addWidget(disk_usage_bar)

    # diskUsageBar -> diskUsageBarValue
    disk_usage_bar_value = QLabel()
    disk_usage_bar_value.setObjectName(f'diskUsageBarValue{card_num}')
    disk_usage_bar_value.setStyleSheet('QLabel#diskUsageBarValue' + str(card_num) + '{min-height: 10px; border-radius: 4px; background-color: #5468ff; min-width: 0px;}')
    disk_usage_bar_layout.addWidget(disk_usage_bar_value)

    # diskUsageBar -> horizontalSpacer
    disk_usage_bar_layout.addSpacerItem(QSpacerItem(40,20, QSizePolicy.Expanding))

    #### end::Disk Usage ####

    # cardContent -> btnSeeMore
    btn_see_more = QPushButton('See more')
    btn_see_more.setObjectName(f'btnSeeMore{card_num}')
    btn_see_more.setStyleSheet('QPushButton#btnSeeMore' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: #5568fe; background-color: transparent; padding: 0px; margin-top: 10px;}')
    btn_see_more.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    card_content_layout.addWidget(btn_see_more, alignment=QtCore.Qt.AlignLeft)

    # cardContent -> btnSeeLess
    btn_see_less = QPushButton('See less')
    btn_see_less.setObjectName(f'btnSeeLess{card_num}')
    btn_see_less.setStyleSheet('QPushButton#btnSeeLess' + str(card_num) + '{font-family: "Segoe UI", sans-serif; font-size: 12px; font-weight: 500; color: #5568fe; background-color: transparent; padding: 0px; margin-top: 10px;}')
    btn_see_less.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    card_content_layout.addWidget(btn_see_less, alignment=QtCore.Qt.AlignLeft)

    # # cardContent -> vertical_spacer
    # vertical_spacer = QSpacerItem(20,40, QSizePolicy.Expanding)
    # card_content_layout.addSpacerItem(vertical_spacer)

    # add the widgets
    card_layout.addWidget(card_header, alignment=QtCore.Qt.AlignTop)
    card_layout.addWidget(card_content)

    # add the new card to cards
    if card_num <= 6:
        row, col = divmod(card_num - 1, 3)
        cards_layout.addWidget(card, row, col, alignment=QtCore.Qt.AlignTop)


