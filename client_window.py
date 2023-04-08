import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic
import json

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

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("client.ui", self)

        # Connect button to start_client function
        self.btnConnect.clicked.connect(self.start_client)

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
