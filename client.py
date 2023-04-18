import json
import socket
import time
from monitor import *

# Set constants
IDLE_TIME_THRESHOLD = 300 # 5 minutes
CPU_USAGE_IDLE_THRESHOLD = 10 # 10%

def connect_to_server(s, callback=None):
    network_info = get_network_info()
    os_info = get_os_info()
    system_info = {"network_info": network_info, "os_info": os_info}
    s.sendall(json.dumps(system_info).encode('utf-8'))

    # Initialize the idle timer
    idle_time = 0

    while True:
        cpu_usage = get_cpu_usage()
        used_memory_usage = get_memory_usage()['used']
        total_memory_usage = get_memory_usage()['total']
        used_disk_usage = get_disk_usage()['used']
        total_disk_usage = get_disk_usage()['total']

        # Update the idle timer
        if cpu_usage < CPU_USAGE_IDLE_THRESHOLD:                    
            idle_time += 1
        else:
            idle_time = 0

        # If the idle timer exceeds the threshold, shut down the system
        if idle_time >= IDLE_TIME_THRESHOLD:
            print("Client will shutdown...")
            s.sendall(json.dumps({"action": "shutdown"}).encode('utf-8'))
            shutdown_system()
            break

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
