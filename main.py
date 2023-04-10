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
    cpu_data_changed = pyqtSignal(str)
    memory_data_changed = pyqtSignal(str)
    disk_data_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            # Get CPU usage live data and format it
            cpu_usage = monitor.get_cpu_usage()
            cpu_usage_formatted = "{:.2f}".format(cpu_usage) + "%"
            print(f'CPU Usage: {cpu_usage_formatted}')

            # Get memory usage live data
            memory_usage = monitor.get_memory_usage()
            memory_usage_formatted = f"{memory_usage['available']} MB / {memory_usage['total']} MB" 
            print(f'Memory Usage: {memory_usage_formatted}')

            # Get disk usage
            disk_usage = monitor.get_disk_usage()
            disk_usage_formatted = f"{disk_usage['available']} MB / {disk_usage['total']} MB" 
            print(f'Disk Usage: {disk_usage_formatted}')
            
            # Emit signal with updated data
            self.cpu_data_changed.emit(cpu_usage_formatted)
            self.memory_data_changed.emit(memory_usage_formatted)
            self.disk_data_changed.emit(disk_usage_formatted)
            
            # Wait for 1 second before updating again
            time.sleep(1)

    def stop(self):
        self.running = False

       
class MainWindow(CustomWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Hide pcDetails
        self.pcDetails.setVisible(False)

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
        self.btnSeeAll.clicked.connect(self.see_all)
        self.btnSettings.enterEvent = lambda event: self.hover_entered(event, "btnSettings")
        self.btnSettings.leaveEvent = lambda event: self.hover_left(event, "btnSettings")
        self.btnLogout.enterEvent = lambda event: self.hover_entered(event, "btnLogout")
        self.btnLogout.leaveEvent = lambda event: self.hover_left(event, "btnLogout")

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)


        # ------------ TESTING PURPOSES ------------------
        # create_new_card(self)

        # # Threads
        # self.live_update_thread = LiveUpdateThread()
        # self.live_update_thread.cpu_data_changed.connect(self.update_cpu_usage)
        # self.live_update_thread.memory_data_changed.connect(self.update_memory_usage)
        # self.live_update_thread.disk_data_changed.connect(self.update_disk_usage)
        # self.live_update_thread.start()

        # self.server_thread = ServerThread('0.0.0.0', 5000, Signal())
        # self.server_thread.signal.hostname_changed.connect(self.update_client_hostname)
        # self.server_thread.signal.cpu_data_changed.connect(self.update_client_cpu_usage)
        # self.server_thread.start()

        # # Hide pcDetails
        # self.pcDetails.setVisible(False)

        # # Set window size for Main
        # self.resize(1280,720)
        # # center window
        # center(self)
        # self.stackedWidget.setCurrentIndex(1)  # Switch to the main page
        # ------------ TESTING PURPOSES ------------------

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

    def update_cpu_usage(self, data):
        # Set CPU usage to widget
        cpu_usage = float(data[:-1])
        self.cpuUsageValueText.setText(data)
        self.cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * cpu_usage))

    def update_memory_usage(self, data):
        # Set memory usage to widget
        self.txtMemoryUsage.setText(data)

    def update_disk_usage(self, data):
        # Set memory usage to widget
        self.txtDiskUsage.setText(data)

    # Update clients
    def update_client_hostname(self, data):
        print(f'Updated client hostname: ', data)
        pc = self.findChild(QPushButton, f'pc{2}')

        if pc is not None:
            pc.setText(f'  {data}')

    def update_client_cpu_usage(self, data):
        cpu_usage = float(data)
        print(f'Updated client cpu usage: ', cpu_usage)
        cpuUsageValueText = self.findChild(QLabel, f'cpuUsageValueText{2}')
        cpuUsageValue = self.findChild(QLabel, f'cpuUsageValue{2}')
        cpuUsageBar = self.findChild(QLabel, f'cpuUsageBar{2}')

        if cpuUsageValueText is not None:
            cpuUsageValueText.setText("{:.2f}".format(cpu_usage) + '%')
            cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * cpu_usage))

    def see_all(self):
        # Show pcDetails
        self.pcDetails.setVisible(True)


    def login(self):
        username = self.txtUsername.text()
        password = self.txtPassword.text()

        # Check the username and password
        if username == 'admin' and password == 'admin':
            # Create thread for updating live data
            self.live_update_thread = LiveUpdateThread()
            self.live_update_thread.cpu_data_changed.connect(self.update_cpu_usage)
            self.live_update_thread.memory_data_changed.connect(self.update_memory_usage)
            self.live_update_thread.disk_data_changed.connect(self.update_disk_usage)
            self.live_update_thread.start()

            # Hide pcDetails
            self.pcDetails.setVisible(False)

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
