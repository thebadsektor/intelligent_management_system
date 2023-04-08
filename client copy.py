import socket
from monitor import get_network_info

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    network_info = get_network_info()
    data = f"{network_info['hostname']} {network_info['ip_address']}"

    client_socket.send(data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")
    
    client_socket.close()

if __name__ == '__main__':
    host = 'YOUR_SERVER_IP_ADDRESS'
    port = 5000
    connect_to_server(host, port)
