import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client {addr} connected")

        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")

        client_socket.send("ack".encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    start_server(host, port)
