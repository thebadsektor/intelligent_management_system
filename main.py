import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import time
from server import start_server, Signal

# Import resources
import resources

# Import utilities
from utils import *

# Import monitor
import monitor

class ServerThread(QThread):
    def __init__(self, host, port, signal):
        super().__init__()
        self.host = host
        self.port = port
        self.signal = signal

    def run(self):
        start_server(self.host, self.port, self.signal)

        
class LiveUpdateThread(QThread):
    cpu_data_changed = pyqtSignal(float)
    memory_data_changed = pyqtSignal(int, int)
    disk_data_changed = pyqtSignal(int, int)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            # Get CPU usage
            cpu_usage = monitor.get_cpu_usage()

            # Get memory usage
            memory_usage = monitor.get_memory_usage()
            available_memory_usage = memory_usage['available']
            total_memory_usage = memory_usage['total']

            # Get disk usage
            disk_usage = monitor.get_disk_usage()
            available_disk_usage = disk_usage['available']
            total_disk_usage = disk_usage['total']
            
            # Emit signal with updated data
            self.cpu_data_changed.emit(cpu_usage)
            self.memory_data_changed.emit(available_memory_usage, total_memory_usage)
            self.disk_data_changed.emit(available_disk_usage, total_disk_usage)
            
            # Wait for 1 second before updating again
            time.sleep(1)

    def stop(self):
        self.running = False

       
class MainWindow(CustomWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set window size for login
        self.resize(440, 500)
        # center window
        center(self)
        self.stackedWidget.setCurrentIndex(0)

        # Initialize mouse_pos attribute
        self.mouse_pos = None

        # Add a QSizeGrip to the bottom-right corner
        size_grip = QSizeGrip(self)
        size_grip.setStyleSheet("background-color: transparent;")
        size_grip.setGeometry(self.rect().right() - 20, self.rect().bottom() - 20, 20, 20)
        size_grip.show()

        # Set title
        self.title.setText('Intelligent Management System')

        # Connections
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnMaximize.clicked.connect(self.toggleMaximized)
        self.btnClose.clicked.connect(self.close)
        self.btnLogin.clicked.connect(self.login)
        self.btnLogout.clicked.connect(self.logout)
        self.btnSettings.enterEvent = lambda event: self.hover_entered(event, "btnSettings")
        self.btnSettings.leaveEvent = lambda event: self.hover_left(event, "btnSettings")
        self.btnLogout.enterEvent = lambda event: self.hover_entered(event, "btnLogout")
        self.btnLogout.leaveEvent = lambda event: self.hover_left(event, "btnLogout")

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
            # Find the button by searching through the child widgets of the main window
            for child_widget in self.findChildren(QPushButton):
                if child_widget.text() == "Login":
                    # Click the button
                    child_widget.click()
                    return True
        
        return super().eventFilter(obj, event)
    

    def hover_entered(self, event, btn_name):
        if btn_name == 'btnSettings':
            self.btnSettings.setIcon(QIcon(':/images/resources/icons_alt/settings.svg'))
        elif btn_name == 'btnLogout':
            self.btnLogout.setIcon(QIcon(':/images/resources/icons_alt/power.svg'))

    def hover_left(self, event, btn_name):
        if btn_name == 'btnSettings':
            self.btnSettings.setIcon(QIcon(':/images/resources/icons_disabled/settings.svg'))
        elif btn_name == 'btnLogout':
            self.btnLogout.setIcon(QIcon(':/images/resources/icons_disabled/power.svg'))

    # PC SERVER
    def update_server_cpu_usage(self, cpu_usage):
        self.cpuUsageValueText.setText("{:.2f}".format(cpu_usage) + "%")
        self.cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * cpu_usage))

    def update_server_memory_usage(self, available_memory_usage, total_memory_usage):
        self.memoryUsageText.setText(f"{available_memory_usage}MB / {total_memory_usage}MB")
        self.memoryUsageBarValue.setFixedWidth(int((self.memoryUsageBar.width()/100) * (available_memory_usage/total_memory_usage)*100))

    def update_server_disk_usage(self, available_disk_usage, total_disk_usage):
        self.diskUsageText.setText(f"{available_disk_usage}MB / {total_disk_usage}MB")
        self.diskUsageBarValue.setFixedWidth(int((self.diskUsageBar.width()/100) * (available_disk_usage/total_disk_usage)*100))

    # PC CLIENT/S
    def spawn_cards(self):
        create_new_card(self)
    
    def update_client_hostname(self, client_num, hostname):
        pc = self.findChild(QPushButton, f'pc{client_num}')
        if pc is not None:
            pc.setText(f'  {hostname}')

    def update_client_cpu_usage(self, client_num, cpu_usage):
        cpuUsageValueText = self.findChild(QLabel, f'cpuUsageValueText{client_num}')
        cpuUsageValue = self.findChild(QLabel, f'cpuUsageValue{client_num}')
        cpuUsageBar = self.findChild(QLabel, f'cpuUsageBar{client_num}')

        if cpuUsageValueText is not None:
            cpuUsageValueText.setText(f"{cpu_usage}%")
            cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * float(cpu_usage)))

    def update_client_memory_usage(self, client_num, available_memory_usage, total_memory_usage):
        memoryUsageText = self.findChild(QLabel, f'memoryUsageText{client_num}')
        memoryUsageBarValue = self.findChild(QLabel, f'memoryUsageBarValue{client_num}')
        memoryUsageBar = self.findChild(QLabel, f'memoryUsageBar{client_num}')

        if memoryUsageText is not None:
            self.memoryUsageText.setText(f"{available_memory_usage}MB / {total_memory_usage}MB")
            self.memoryUsageBarValue.setFixedWidth(int((self.memoryUsageBar.width()/100) * (available_memory_usage/total_memory_usage)*100))

    def see_more(self):
        # See more
        self.btnSeeMore.setVisible(False)
        self.btnSeeLess.setVisible(True)
        self.memoryUsage.setVisible(True)
        self.memoryUsageBar.setVisible(True)
        self.diskUsage.setVisible(True)
        self.diskUsageBar.setVisible(True)
        self.card.setMaximumHeight(255)
        self.header.setFocus()
    
    def see_less(self):
        # See less
        self.btnSeeMore.setVisible(True)
        self.btnSeeLess.setVisible(False)
        self.memoryUsage.setVisible(False)
        self.memoryUsageBar.setVisible(False)
        self.diskUsage.setVisible(False)
        self.diskUsageBar.setVisible(False)
        self.card.setMaximumHeight(130)
        self.header.setFocus()

    def login(self):
        username = self.txtUsername.text()
        password = self.txtPassword.text()

        # Check the username and password
        if username == 'admin' and password == 'admin':
            # Threads
            self.live_update_thread = LiveUpdateThread()
            self.live_update_thread.cpu_data_changed.connect(self.update_server_cpu_usage)
            self.live_update_thread.memory_data_changed.connect(self.update_server_memory_usage)
            self.live_update_thread.disk_data_changed.connect(self.update_server_disk_usage)
            self.live_update_thread.start()

            self.server_thread = ServerThread('0.0.0.0', 5000, Signal())
            self.server_thread.signal.new_client_connected.connect(self.spawn_cards)
            self.server_thread.signal.hostname_changed.connect(self.update_client_hostname)
            self.server_thread.signal.cpu_data_changed.connect(self.update_client_cpu_usage)
            self.server_thread.signal.memory_data_changed.connect(self.update_client_memory_usage)
            self.server_thread.start()
            
            self.btnSeeMore.clicked.connect(self.see_more)
            self.btnSeeLess.clicked.connect(self.see_less)

            # See less
            self.btnSeeMore.setVisible(True)
            self.btnSeeLess.setVisible(False)
            self.memoryUsage.setVisible(False)
            self.memoryUsageBar.setVisible(False)
            self.diskUsage.setVisible(False)
            self.diskUsageBar.setVisible(False)
            self.card.setMaximumHeight(130)

            # Set window size for Main
            self.resize(1000, 600)
            
            # set focus on header
            self.header.setFocus()

            # center window
            center(self)
            self.stackedWidget.setCurrentIndex(1)  # Switch to the main page
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid username or password.')

    def logout(self):
        # Clear login credentials
        self.txtUsername.setText('')
        self.txtPassword.setText('')

        # Set focus to header
        self.header.setFocus()

        # Set window size for login
        self.resize(440,600)

        # center window
        center(self)

        self.stackedWidget.setCurrentIndex(0)  # Switch to the login page
        self.live_update_thread.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
