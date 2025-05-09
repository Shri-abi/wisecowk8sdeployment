#!/usr/bin/env python3

import psutil
import logging
from datetime import datetime

MAX_CPU = 80       # CPU usage threshold in percent
MAX_MEMORY = 80    # Memory usage threshold in percent
MAX_DISK = 90      # Disk usage threshold in percent

# Log configuration
LOG_PATH = "system_health.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def alert(message):
    """Logs and prints alert messages for threshold breaches."""
    print(f"ALERT: {message}")
    logging.warning(message)

def monitor():
    """Performs system resource checks and logs any threshold violations."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    total_processes = len(psutil.pids())

    print(f"System Status @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"CPU: {cpu_usage}% | Memory: {memory_usage}% | Disk: {disk_usage}% | Active Processes: {total_processes}")

    if cpu_usage > MAX_CPU:
        alert(f"CPU usage is high: {cpu_usage}%")
    if memory_usage > MAX_MEMORY:
        alert(f"Memory usage is high: {memory_usage}%")
    if disk_usage > MAX_DISK:
        alert(f"Disk usage is critical: {disk_usage}%")

if __name__ == "__main__":
    monitor()

