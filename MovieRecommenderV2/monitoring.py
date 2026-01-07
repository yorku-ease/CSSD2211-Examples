import psutil
import time
import csv
import os

PROCESS_NAMES = ["python.exe"]  # could refine if multiple Python apps are running
STOP_FILE = "STOP_MONITORING"
INTERVAL = 0.5  # seconds

# Reset stop file
if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)

def monitor():
    with open("metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "service_name", "pid", "cpu_percent", "memory_mb"])

        while True:
            if os.path.exists(STOP_FILE):
                print("Stop file detected. Exiting monitoring...")
                break

            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["name"] in PROCESS_NAMES:
                    # Attempt to read SERVICE_NAME from process environment
                    service_name = None
                    try:
                        env = proc.environ()
                        service_name = env.get("SERVICE_NAME", "unknown")
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        service_name = "unknown_python_process"

                    try:
                        cpu = proc.cpu_percent(interval=0.1)
                        mem = proc.memory_info().rss / (1024 * 1024)
                        writer.writerow([time.time(), service_name, proc.info["pid"], cpu, mem])
                        print(f"{proc.info['name']} (PID {proc.info['pid']}) CPU: {cpu}%, MEM: {mem:.2f} MB")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor()