import json
import socket
import psutil
import time
from monitor import get_network_info, get_os_info, get_cpu_usage, get_memory_usage, get_disk_usage

def connect_to_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # network_info = get_network_info()

        while True:
            data = "hello"
            s.sendall((json.dumps(data)).encode('utf-8'))

            time.sleep(1)
        

if __name__ == '__main__':
    host = 'YOUR_SERVER_IP_ADDRESS'
    port = 5000
    connect_to_server(host, port)
