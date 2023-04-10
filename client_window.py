import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic
import json

# Import resources
import resources

# Import utilities
from utils import *

from client import connect_to_server, get_cpu_usage

class ConnectionThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        connect_to_server(self.host, self.port, callback=self.update_received_data)
        
    def update_received_data(self, data):
        self.data_received.emit(data)

class ClientWindow(CustomWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("client.ui", self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set initial window size for client window
        self.resize(440,600)
        
        # center window
        center(self)

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

        # Connect button to start_client function
        self.btnConnect.clicked.connect(self.start_client)

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
            # Find the button by searching through the child widgets of the main window
            for child_widget in self.findChildren(QPushButton):
                if child_widget.text() == "Connect":
                    # Click the button
                    child_widget.click()
                    return True
        
        return super().eventFilter(obj, event)
    
    def start_client(self):
        host = self.txtServerIP.text()
        port = int(self.txtServerPort.text())
        self.connection_thread = ConnectionThread(host, port)
        self.connection_thread.data_received.connect(self.display_received_data)
        self.connection_thread.start()

    def display_received_data(self, data):
        print(data)
        self.txtReceivedData.setPlainText(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())
