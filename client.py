import json
import socket
import psutil
import time
from monitor import get_network_info, get_os_info

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def connect_to_server(host, port, callback=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        network_info = get_network_info()
        os_info = get_os_info()
        system_info = {"network_info": network_info, "os_info": os_info}
        s.sendall(json.dumps(system_info).encode('utf-8'))

        while True:
            cpu_usage = get_cpu_usage()
            if callback is not None:
                callback(f"Client {network_info['hostname']} - {network_info['ip']} : {cpu_usage}%")
            s.sendall(str(cpu_usage).encode('utf-8'))
            time.sleep(1)  # Send CPU usage every 1 second

if __name__ == '__main__':
    host = 'YOUR_SERVER_IP_ADDRESS'
    port = 5000
    connect_to_server(host, port)
