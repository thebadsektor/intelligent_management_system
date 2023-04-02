import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic

# Import resources
import resources

# Import utilities
from utils import *

# Import monitor
import monitor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set initial window size for Login
        self.resize(460,600)

        # Initialize mouse_pos attribute
        self.mouse_pos = None

        # Add a QSizeGrip to the bottom-right corner
        size_grip = QSizeGrip(self)
        size_grip.setStyleSheet("background-color: transparent;")
        size_grip.setGeometry(self.rect().right() - 20, self.rect().bottom() - 20, 20, 20)
        size_grip.show()

        # Set stackedWidget as centralWidget
        # self.setCentralWidget(self.stackedWidget)

        # Set title
        self.setWindowTitle('Intelligent Management System')

        # Connections
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnMaximize.clicked.connect(self.toggleMaximized)
        self.btnClose.clicked.connect(self.close)
        self.btnLogin.clicked.connect(self.login)

    def update_cpu_usage(self):
        # Get CPU usage
        cpu_usage = monitor.get_cpu_usage()
        cpu_usage_formatted = "{:.2f}".format(cpu_usage) + "%"
        print(f'CPU Usage: {cpu_usage_formatted}')

        # Set CPU usage to widget
        self.cpuUsageValueText.setText(cpu_usage_formatted)
        self.cpuUsageValue.setFixedWidth((self.cpuUsageBar.width()/100) * cpu_usage)

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

    # Override the resizeEvent to move the QSizeGrip with the window
    def resizeEvent(self, event):
        size_grip = self.findChild(QSizeGrip)
        size_grip.setGeometry(self.rect().right() - 20, self.rect().bottom() - 20, 20, 20)
        super().resizeEvent(event)

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
            self.btnMaximize.setStyleSheet("QPushButton {image: url(:/images/resources/icons/square_alt.svg); min-width: 16px; min-height: 16px;max-width: 16px; max-height: 16px;padding-top: 10px;padding-bottom: 10px;padding-left: 20px;padding-right: 20px;} QPushButton:hover {background-color: #3d4145;}")
        else:
            self.showMaximized()
            self.btnMaximize.setStyleSheet("QPushButton {image: url(:/images/resources/icons/copy.svg); min-width: 16px; min-height: 16px;max-width: 16px; max-height: 16px;padding-top: 10px;padding-bottom: 10px;padding-left: 20px;padding-right: 20px;} QPushButton:hover {background-color: #3d4145;}")

    def login(self):
        username = self.txtUsername.text()
        password = self.txtPassword.text()

        # Check the username and password
        if username == 'admin' and password == 'admin':
            # Set up QTimer to update CPU usage every second
            self.update_cpu_usage()
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_cpu_usage)
            self.timer.start(1000) # 1000 ms = 1 second

            # Set window size for Main
            self.resize(1280,720)
            # center window
            center(self)
            self.stackedWidget.setCurrentIndex(1)  # Switch to the main page
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid username or password.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
