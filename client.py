import json
import socket
import time
from monitor import get_network_info, get_os_info, get_cpu_usage, get_memory_usage, get_disk_usage

def connect_to_server(host, port, callback=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        network_info = get_network_info()
        os_info = get_os_info()
        system_info = {"network_info": network_info, "os_info": os_info}
        s.sendall(json.dumps(system_info).encode('utf-8'))

        while True:
            cpu_usage = get_cpu_usage()
            used_memory_usage = get_memory_usage()['used']
            total_memory_usage = get_memory_usage()['total']
            used_disk_usage = get_disk_usage()['used']
            total_disk_usage = get_disk_usage()['total']

            if callback is not None:
                callback(f"Client {network_info['hostname']} - {network_info['ip_address']} : {cpu_usage}%")

            data = {
                "cpu_usage": "{:.2f}".format(cpu_usage), 
                "used_memory_usage": round(used_memory_usage / 1024, 2), 
                "total_memory_usage": round(total_memory_usage / 1024, 2),
                "used_disk_usage": round(used_disk_usage / 1024, 2),
                "total_disk_usage": round(total_disk_usage / 1024, 2)}

            s.sendall(json.dumps(data).encode('utf-8'))

            # Wait every 1 second before sending again
            time.sleep(1)
        

if __name__ == '__main__':
    host = 'YOUR_SERVER_IP_ADDRESS'
    port = 5000
    connect_to_server(host, port)
