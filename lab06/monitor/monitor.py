import psutil
import time
import platform
import socket
import logging

logging.basicConfig(level=logging.INFO, filename="system_monitor.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def log_info(category, message):
    logger.info(f"{category} - {message}")
    print(f"{category} - {message}")
    
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    
    log_info("CPU", f"CPU Usage: {cpu_percent}%")
    log_info("Memory", f"Memory Usage: {memory_info.percent}%")
    
def monitor_system_info():
    os_info = platform.uname()
    hostname = socket.gethostname()
    
    log_info("System info", f"Hostname: {hostname}")
    log_info("System info", f"Operating System: {os_info.system} {os_info.release}")
    log_info("System info", f"Python Version: {platform.python_version()}")
    
def monitor_network():
    net_stats = psutil.net_io_counters()
    log_info("Network", f"Bytes Sent: {net_stats.bytes_sent}, Bytes Received: {net_stats.bytes_recv}")

def monitor_software():
    software_list = psutil.process_iter(attrs=['pid', 'name', 'username'])
    
    log_info("Software", "List of running software:")
    for software in software_list:
        software_name = software.info['name']
        software_pid = software.info['pid']
        software_username = software.info['username']
        log_info("Software", f"Name: {software_name}, PID: {software_pid}, Username: {software_username}")
        
def monitor_system():
    log_info("System", "Start Monitoring system...")
    while True:
        monitor_cpu_memory()
        monitor_system_info()
        monitor_network()
        monitor_software()
        log_info("System Monitor", 
                 "------------------------------------------------")
        time.sleep(60)
        
if __name__ == "__main__":
    monitor_system()