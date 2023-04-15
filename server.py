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

    data = json.loads(client_socket.recv(1024).decode('utf-8'))
    print(f'START: {data}')

    with client_socket:
        while True:
            data = json.loads(client_socket.recv(1024).decode('utf-8'))
            print(f'DATA: {data}')


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
