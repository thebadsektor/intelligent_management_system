import json
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal

from utils import *

class Signal(QObject):
    new_client_connected = pyqtSignal(int)
    remove_client = pyqtSignal(int)
    hostname_changed = pyqtSignal(int, str)
    cpu_data_changed = pyqtSignal(int, str)
    memory_data_changed = pyqtSignal(int, float, float)
    disk_data_changed = pyqtSignal(int, float, float)

def handle_client(client_socket, addr, signal, client_num):
    print(f"Client #{client_num} {addr} connected")

    system_info = json.loads(client_socket.recv(1024).decode('utf-8'))
    network_info = system_info['network_info']

    signal.hostname_changed.emit(client_num, network_info['hostname'])

    with client_socket:
        while True:
            data = json.loads(client_socket.recv(1024).decode('utf-8'))
            print(data)

            # Check if the action is to shutdown the client
            if 'action' in data and data['action'] == 'shutdown':
                print(f"Shutting down client for Client #{client_num}")
                signal.remove_client.emit(client_num)
                break
            
            signal.cpu_data_changed.emit(client_num, data['cpu_usage'])
            signal.memory_data_changed.emit(client_num, data['used_memory_usage'], data['total_memory_usage'])
            signal.disk_data_changed.emit(client_num, data['used_disk_usage'], data['total_disk_usage'])
            
        # emit remove_client signal when client socket is closed
        print("Client is disconnecting")
        signal.remove_client.emit(client_num)

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
            signal.new_client_connected.emit(client_num)
            client_num += 1

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    start_server(host, port)
