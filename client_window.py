import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic
import json
from utils import *
import socket

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
        self.socket = None

    def run(self):
        self.socket = connect_to_server(self.host, self.port, callback=self.update_received_data)

    def send_message(self, message):
        if self.socket is not None:
            data = json.dumps({'message': message}).encode('utf-8')
            self.socket.sendall(data)
        else:
            print("Socket is not connected.")
        
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
        self.txtServerIP.textChanged.connect(self.client_text_changed)
        self.txtServerPort.textChanged.connect(self.client_text_changed)

        # Check client inputs
        self.check_client_inputs(self.txtServerIP.text(), self.txtServerPort.text())

        # only allow numbers in txtServerPort
        int_validator = QIntValidator()
        self.txtServerPort.setValidator(int_validator)

        # Install an event filter on the application to intercept key events
        app = QApplication.instance()
        app.installEventFilter(self)

    # Handle Enter key pressed in connect
    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
            btnConnect = self.findChild(QPushButton, "btnConnect")
            if btnConnect and btnConnect.isVisible():
                btnConnect.click()
                return True
        return super().eventFilter(obj, event)
    
    def check_client_inputs(self, server_ip_text, server_port_text):
        # If no inputs
        if not server_ip_text or not server_port_text:
            print('disabled')
            self.btnConnect.setEnabled(False)
            self.btnConnect.setStyleSheet('background-color: #4E5BBC')
        # Has input
        else:
            self.btnConnect.setEnabled(True)
            self.btnConnect.setStyleSheet('background-color: #5468ff')

    def client_text_changed(self):
        server_ip_text = self.txtServerIP.text().strip()
        server_port_text = self.txtServerPort.text().strip()

        # Ensure that the text in txtServerIP consists only of numbers and periods
        if not all(char.isdigit() or char == '.' for char in server_ip_text):
            server_ip_text = ''.join(char for char in server_ip_text if char.isdigit() or char == '.')

        # Update txtServerIP
        self.txtServerIP.setText(server_ip_text)

        self.check_client_inputs(server_ip_text, server_port_text)
        
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
            self.connection_thread.send_message('Client disconnected')
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
