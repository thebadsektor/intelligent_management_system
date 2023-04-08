import socket
import threading

def handle_client(client_socket):
    with client_socket:
        while True:
            cpu_usage = client_socket.recv(1024).decode('utf-8')
            if not cpu_usage:
                break
            print(f'Client CPU Usage: {cpu_usage}%')

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, addr = s.accept()
            print(f"Client {addr} connected")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    start_server(host, port)
