import json
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class Signal(QObject):
    hostname_changed = pyqtSignal(str)
    cpu_data_changed = pyqtSignal(str)

# signal = Signal()

def handle_client(client_socket, addr, signal):
    print(f"Client {addr} connected")
    
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
            if not cpu_usage:
                break
            print(f'Client {network_info["hostname"]} CPU Usage: {cpu_usage}%')
            signal.hostname_changed.emit(network_info['hostname'])
            signal.cpu_data_changed.emit(cpu_usage)


def start_server(host, port, signal):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr, signal))
            thread.start()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    start_server(host, port)
