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

# Define a function to get the idle time in seconds
def get_idle_time():
    return (psutil.cpu_times().idle + psutil.cpu_times().iowait)

# Define a function to send the shutdown command to the OS
def shutdown_system():
    if os.name == "posix":
        os.system("sudo shutdown -h now")
    elif os.name == "nt":
        os.system("shutdown /s /t 0")

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'total': memory.total // (1024*1024),
        'used': memory.used // (1024*1024),
        'available': memory.available // (1024*1024)
    }

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total // (1024*1024),
        'used': disk.used // (1024*1024),
        'available': disk.free // (1024*1024)
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
