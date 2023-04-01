import os
import platform
import psutil
import socket
import time
from datetime import timedelta

def get_hostname():
    return socket.gethostname()

def get_os_info():
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version()
    }

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'used': memory.used,
        'available': memory.available
    }

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total,
        'used': disk.used,
        'available': disk.free
    }

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {
        'hostname': hostname,
        'ip_address': ip_address
    }

def get_running_processes():
    processes = [proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']) for proc in psutil.process_iter()]
    return processes

def get_uptime():
    return timedelta(seconds=int(time.time() - psutil.boot_time()))

def main():
    pc_info = {
        'hostname': get_hostname(),
        'os_info': get_os_info(),
        'cpu_usage': get_cpu_usage(),
        'memory_usage': get_memory_usage(),
        'disk_usage': get_disk_usage(),
        'network_info': get_network_info(),
        'running_processes': get_running_processes(),
        'uptime': get_uptime()
    }
    
    for key, value in pc_info.items():
        print(f'{key}: {value}')

if __name__ == '__main__':
    main()
