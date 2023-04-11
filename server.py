import json
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal

from utils import *

class Signal(QObject):
    new_client_connected = pyqtSignal()
    hostname_changed = pyqtSignal(int, str)
    cpu_data_changed = pyqtSignal(int, str)
    memory_data_changed = pyqtSignal(int, int, int)

def handle_client(client_socket, addr, signal, client_num):
    print(f"Client #{client_num} {addr} connected")
    
    with client_socket:
        # Receive system_info from the client
        system_info = json.loads(client_socket.recv(1024).decode('utf-8'))
        network_info = system_info["network_info"]
        os_info = system_info["os_info"]
        print(f"Received network_info: {network_info}")
        print(f"Received os_info: {os_info}")

        # Keep receiving data from the client
        while True:
            cpu_usage = client_socket.recv(1024).decode('utf-8')

            signal.hostname_changed.emit(client_num, network_info['hostname'])

            if cpu_usage:
                signal.cpu_data_changed.emit(client_num, cpu_usage)
                # signal.memory_data_changed.emit(client_num, available_memory_usage, total_memory_usage)


def start_server(host, port, signal):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        client_num = 2

        while True:
            client_socket, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr, signal, client_num))
            thread.start()
            signal.new_client_connected.emit()
            client_num += 1

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    start_server(host, port)
