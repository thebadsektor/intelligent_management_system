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

from client import connect_to_server

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

        # Hide disconnect button
        self.btnDisconnect.setVisible(False)

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
        self.btnConnect.clicked.connect(self.start_client)
        self.btnDisconnect.clicked.connect(self.stop_client)

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
            # Find the button by searching through the child widgets of the main window
            btnConnect = self.findChild(QPushButton, "btnConnnect")
            for child_widget in self.findChildren(QPushButton):
                if child_widget.text() == "Connect" and btnConnect.isVisible() :
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

        # Changes in UI
        self.txtTitle.setText('Connected')
        self.txtServerIP.setEnabled(False)
        self.txtServerIP.setStyleSheet('margin-bottom: 15px; background-color: #22242C;')
        self.txtServerPort.setEnabled(False)
        self.txtServerPort.setStyleSheet('margin-bottom: 15px; background-color: #22242C;')
        self.btnConnect.setVisible(False)
        self.btnDisconnect.setVisible(True)


    def stop_client(self):
        if hasattr(self, 'connection_thread') and self.connection_thread.isRunning():
            self.connection_thread.terminate()
            self.connection_thread.wait()
            del self.connection_thread

        # Changes in UI
        self.txtTitle.setText('Connect to Server')
        self.txtServerIP.setEnabled(True)
        self.txtServerIP.setStyleSheet('margin-bottom: 15px;')
        self.txtServerPort.setEnabled(True)
        self.txtServerPort.setStyleSheet('margin-bottom: 15px;')
        self.btnDisconnect.setVisible(False)
        self.btnConnect.setVisible(True)

    def display_received_data(self, data):
        print(data)
        self.txtReceivedData.setPlainText(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())
