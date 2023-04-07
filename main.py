import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import time
from server import start_server

# Import resources
import resources

# Import utilities
from utils import *

# Import monitor
import monitor

class ServerThread(QThread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        start_server(self.host, self.port)
        
class LiveUpdateThread(QThread):
    data_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            # Get CPU usage live data and format it
            cpu_usage = monitor.get_cpu_usage()
            cpu_usage_formatted = "{:.2f}".format(cpu_usage) + "%"
            print(f'CPU Usage: {cpu_usage_formatted}')
            
            # Emit signal with updated data
            self.data_changed.emit(cpu_usage_formatted)
            
            # Wait for 1 second before updating again
            time.sleep(1)

    def stop(self):
        self.running = False

       
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.server_thread = ServerThread('0.0.0.0', 5000)
        self.server_thread.start()

        
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

    def update_live_data(self, data):
        # Set CPU usage to widget
        cpu_usage = float(data[:-1])
        self.cpuUsageValueText.setText(data)
        self.cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * cpu_usage))
        
    def closeEvent(self, event):
        self.live_update_thread.stop()
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
            # Create thread for updating live data
            self.live_update_thread = LiveUpdateThread()
            self.live_update_thread.data_changed.connect(self.update_live_data)
            self.live_update_thread.start()

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
