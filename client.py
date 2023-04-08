import socket
import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def connect_to_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            cpu_usage = get_cpu_usage()
            s.sendall(str(cpu_usage).encode('utf-8'))
            time.sleep(1)  # Send CPU usage every 1 second

if __name__ == '__main__':
    host = 'YOUR_SERVER_IP_ADDRESS'
    port = 5000
    connect_to_server(host, port)
