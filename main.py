import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import time
from server import start_server, Signal
import json
import subprocess

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
    memory_data_changed = pyqtSignal(float, float)
    disk_data_changed = pyqtSignal(float, float)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            # Get CPU usage
            cpu_usage = monitor.get_cpu_usage()

            # Get memory usage
            memory_usage = monitor.get_memory_usage()
            used_memory_usage = round(memory_usage['used'] / 1024, 2)
            total_memory_usage = round(memory_usage['total'] / 1024, 2)

            # Get disk usage
            disk_usage = monitor.get_disk_usage()
            used_disk_usage = round(disk_usage['used'] / 1024, 2)
            total_disk_usage = round(disk_usage['total'] / 1024, 2)
            
            # Emit signal with updated data
            self.cpu_data_changed.emit(cpu_usage)
            self.memory_data_changed.emit(used_memory_usage, total_memory_usage)
            self.disk_data_changed.emit(used_disk_usage, total_disk_usage)
            
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
        self.btnActivity.enterEvent = lambda event: self.hover_entered(event, "btnActivity")
        self.btnActivity.leaveEvent = lambda event: self.hover_left(event, "btnActivity")
        self.btnSettings.enterEvent = lambda event: self.hover_entered(event, "btnSettings")
        self.btnSettings.leaveEvent = lambda event: self.hover_left(event, "btnSettings")
        self.btnLogout.enterEvent = lambda event: self.hover_entered(event, "btnLogout")
        self.btnLogout.leaveEvent = lambda event: self.hover_left(event, "btnLogout")
        self.btnActivity.clicked.connect(self.open_activity)
        self.btnSettings.clicked.connect(self.open_settings)
        self.txtServerName.textChanged.connect(self.settings_text_changed)
        self.btnSave.clicked.connect(self.settings_save)

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)

    # Handle Enter key pressed in login
    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
            btnLogin = self.findChild(QPushButton, "btnLogin")
            if btnLogin and btnLogin.isVisible():
                btnLogin.click()
                return True
        return super().eventFilter(obj, event)
    
    def open_activity(self):
        self.btnActivity.setIcon(QIcon(':/images/resources/icons_alt/activity.svg'))
        self.btnSettings.setIcon(QIcon(':/images/resources/icons_disabled/settings.svg'))

        # Set from settings.json
        set_from_settings(self)

        self.stackedWidget2.setCurrentIndex(0)

    def open_settings(self): 
        self.btnSettings.setIcon(QIcon(':/images/resources/icons_alt/settings.svg'))
        self.btnActivity.setIcon(QIcon(':/images/resources/icons_disabled/activity.svg'))

        # # only allow numbers in txtIdleTimes and txtCpuUsageIdleThreshold
        # int_validator = QIntValidator()
        # self.txtIdleTime.setValidator(int_validator)
        # self.txtCpuUsageIdleThreshold.setValidator(int_validator)

        # Set settings inputs
        set_settings_inputs(self)

        # Check settings inputs
        self.check_settings_inputs(self.txtServerName.text())

        self.stackedWidget2.setCurrentIndex(1)

    def check_settings_inputs(self, server_name_text):
        # If no input
        if not server_name_text:
            print('disabled')
            self.btnSave.setEnabled(False)
            self.btnSave.setStyleSheet('background: #4E5BBC')
        # Has input
        else:
            self.btnSave.setEnabled(True)
            self.btnSave.setStyleSheet('background: #5468ff')

    def settings_text_changed(self):
        server_name_text = self.txtServerName.text().strip()
        self.check_settings_inputs(server_name_text)

    def settings_save(self):
        # Load the data from the file
        with open('settings.json') as f:
            data = json.load(f)

        # Update the settings.json values
        data['server_name'] = self.txtServerName.text()

        # Write the updated data back to the file
        with open('settings.json', 'w') as f:
            json.dump(data, f)

        # Create a message box object
        msgBox = QMessageBox()
        msgBox.setText("Settings has been updated")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.addButton(QMessageBox.Ok)
        msgBox.setWindowTitle("Settings")
        msgBox.setFixedWidth(400)
        response = msgBox.exec_()

    def hover_entered(self, event, btn_name):
        if btn_name == 'btnActivity':
            self.btnActivity.setIcon(QIcon(':/images/resources/icons_alt/activity.svg'))
        elif btn_name == 'btnSettings':
            self.btnSettings.setIcon(QIcon(':/images/resources/icons_alt/settings.svg'))
        elif btn_name == 'btnLogout':
            self.btnLogout.setIcon(QIcon(':/images/resources/icons_alt/power.svg'))

    def hover_left(self, event, btn_name):
        if btn_name == "btnActivity":
            if self.stackedWidget2.currentIndex() == 0:
                self.btnActivity.setIcon(QIcon(':/images/resources/icons_alt/activity.svg'))
            else:
                self.btnActivity.setIcon(QIcon(':/images/resources/icons_disabled/activity.svg'))
        elif btn_name == 'btnSettings':
            if self.stackedWidget2.currentIndex() == 1:
                self.btnSettings.setIcon(QIcon(':/images/resources/icons_alt/settings.svg'))
            else:
                self.btnSettings.setIcon(QIcon(':/images/resources/icons_disabled/settings.svg'))
        elif btn_name == 'btnLogout':
            self.btnLogout.setIcon(QIcon(':/images/resources/icons_disabled/power.svg'))

    # PC SERVER
    def update_server_cpu_usage(self, cpu_usage):
        self.cpuUsageValueText.setText("{:.2f}".format(cpu_usage) + "%")
        self.cpuUsageValue.setFixedWidth(int((self.cpuUsageBar.width()/100) * cpu_usage))

    def update_server_memory_usage(self, used_memory_usage, total_memory_usage):
        self.memoryUsageText.setText(f"{used_memory_usage} GB / {total_memory_usage} GB")
        self.memoryUsageBarValue.setFixedWidth(int((self.memoryUsageBar.width()/100) * (used_memory_usage/total_memory_usage)*100))

    def update_server_disk_usage(self, used_disk_usage, total_disk_usage):
        self.diskUsageText.setText(f"{used_disk_usage} GB / {total_disk_usage} GB")
        self.diskUsageBarValue.setFixedWidth(int((self.diskUsageBar.width()/100) * (used_disk_usage/total_disk_usage)*100))

    # PC CLIENT/S
    def spawn_cards(self, client_num):
        create_new_card(self, client_num)

        self.scrollArea.setMinimumWidth(self.cards.minimumSizeHint().width())

        btnSeeMore = self.findChild(QPushButton, f'btnSeeMore{client_num}')
        btnSeeLess = self.findChild(QPushButton, f'btnSeeLess{client_num}')

        btnSeeMore.clicked.connect(lambda: self.see_more(client_num))
        btnSeeLess.clicked.connect(lambda: self.see_less(client_num))

        self.see_less(client_num)

    def remove_card(self, client_num):
        card = self.findChild(QFrame, f'card{client_num}')
        cards_layout = self.cards.layout()
        cards_layout.removeWidget(card)

        self.scrollArea.setMinimumWidth(self.cards.minimumSizeHint().width())

    
    def update_client_hostname(self, client_num, hostname):
        pc = self.findChild(QPushButton, f'pc{client_num}')
        if pc is not None:
            pc.setText(f'  {hostname}')

    def update_client_cpu_usage(self, client_num, cpu_usage):
        cpuUsageValueText = self.findChild(QLabel, f'cpuUsageValueText{client_num}')
        cpuUsageValue = self.findChild(QLabel, f'cpuUsageValue{client_num}')
        cpuUsageBar = self.findChild(QFrame, f'cpuUsageBar{client_num}')

        if cpuUsageValueText and cpuUsageValue and cpuUsageBar:
            cpuUsageValueText.setText(f"{cpu_usage}%")
            cpuUsageValue.setFixedWidth(int((cpuUsageBar.width()/100) * float(cpu_usage)))

    def update_client_memory_usage(self, client_num, used_memory_usage, total_memory_usage):
        memoryUsageText = self.findChild(QLabel, f'memoryUsageText{client_num}')
        memoryUsageBarValue = self.findChild(QLabel, f'memoryUsageBarValue{client_num}')
        memoryUsageBar = self.findChild(QFrame, f'memoryUsageBar{client_num}')

        if memoryUsageText and memoryUsageBarValue and memoryUsageBar:
            memoryUsageText.setText(f"{used_memory_usage} GB / {total_memory_usage} GB")
            memoryUsageBarValue.setFixedWidth(int((memoryUsageBar.width()/100) * float((used_memory_usage/total_memory_usage)*100)))

    def update_client_disk_usage(self, client_num, used_disk_usage, total_disk_usage):
        diskUsageText = self.findChild(QLabel, f'diskUsageText{client_num}')
        diskUsageBarValue = self.findChild(QLabel, f'diskUsageBarValue{client_num}')
        diskUsageBar = self.findChild(QFrame, f'diskUsageBar{client_num}')

        if diskUsageText and diskUsageBarValue and diskUsageBar:
            diskUsageText.setText(f"{used_disk_usage} GB / {total_disk_usage} GB")
            diskUsageBarValue.setFixedWidth(int((diskUsageBar.width()/100) * float((used_disk_usage/total_disk_usage)*100)))

    # See more
    def see_more(self, client_num=""):
        btnSeeMore = self.findChild(QPushButton, f'btnSeeMore{client_num}')
        btnSeeLess = self.findChild(QPushButton, f'btnSeeLess{client_num}')
        memoryUsage = self.findChild(QFrame, f'memoryUsage{client_num}')
        memoryUsage = self.findChild(QFrame, f'memoryUsage{client_num}')
        memoryUsageBar = self.findChild(QFrame, f'memoryUsageBar{client_num}')
        diskUsage = self.findChild(QFrame, f'diskUsage{client_num}')
        diskUsageBar = self.findChild(QFrame, f'diskUsageBar{client_num}')
        card = self.findChild(QFrame, f'card{client_num}')

        btnSeeMore.setVisible(False)
        btnSeeLess.setVisible(True)
        memoryUsage.setVisible(True)
        memoryUsageBar.setVisible(True)
        diskUsage.setVisible(True)
        diskUsageBar.setVisible(True)
        card.setMaximumHeight(255)

        self.header.setFocus()
    
    # See less
    def see_less(self, client_num=""):
        btnSeeMore = self.findChild(QPushButton, f'btnSeeMore{client_num}')
        btnSeeLess = self.findChild(QPushButton, f'btnSeeLess{client_num}')
        memoryUsage = self.findChild(QFrame, f'memoryUsage{client_num}')
        memoryUsage = self.findChild(QFrame, f'memoryUsage{client_num}')
        memoryUsageBar = self.findChild(QFrame, f'memoryUsageBar{client_num}')
        diskUsage = self.findChild(QFrame, f'diskUsage{client_num}')
        diskUsageBar = self.findChild(QFrame, f'diskUsageBar{client_num}')
        card = self.findChild(QFrame, f'card{client_num}')

        btnSeeMore.setVisible(True)
        btnSeeLess.setVisible(False)
        memoryUsage.setVisible(False)
        memoryUsageBar.setVisible(False)
        diskUsage.setVisible(False)
        diskUsageBar.setVisible(False)
        card.setMaximumHeight(130)

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
            self.server_thread.signal.remove_client.connect(self.remove_card)
            self.server_thread.signal.hostname_changed.connect(self.update_client_hostname)
            self.server_thread.signal.cpu_data_changed.connect(self.update_client_cpu_usage)
            self.server_thread.signal.memory_data_changed.connect(self.update_client_memory_usage)
            self.server_thread.signal.disk_data_changed.connect(self.update_client_disk_usage)
            self.server_thread.start()

            self.scrollArea.setMinimumWidth(self.cards.minimumSizeHint().width())
            
            self.btnSeeMore.clicked.connect(lambda: self.see_more())
            self.btnSeeLess.clicked.connect(lambda: self.see_less())
            
            # See less
            self.see_less()

            # Set window size for Main
            self.resize(1000, 600)

            # center window
            center(self)

            # switch to main page
            self.stackedWidget.setCurrentIndex(1)  # Switch to the main page

            # switch to activity page
            self.open_activity()
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
