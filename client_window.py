import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout
from PyQt5 import uic

from client import connect_to_server

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("client.ui", self)

        # Connect button to connect_to_server function
        self.btnConnect.clicked.connect(self.start_client)

    def start_client(self):
        host = self.txtServerIP.text()
        port = int(self.txtServerPort.text())
        received_data = connect_to_server(host, port)

        self.txtReceivedData.setPlainText(received_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())
