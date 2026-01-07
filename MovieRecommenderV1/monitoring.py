import psutil
import csv
import time
import os

PROCESS_NAME = "python.exe"
INTERVAL = 0.5
OUTPUT_FILE = "metrics.csv"
STOP_FILE = "STOP_MONITORING"

# Remove old stop file if it exists
if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)

def monitor():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "memory_mb"])

        # Initialize CPU counters
        procs = [p for p in psutil.process_iter(["name"]) if p.info["name"].lower() == PROCESS_NAME.lower()]
        for p in procs:
            try:
                p.cpu_percent(interval=0.1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        while True:
            if os.path.exists(STOP_FILE):
                print("Stop file detected. Exiting monitoring...")
                break

            timestamp = time.time()
            total_cpu = 0.0
            total_mem = 0.0
            procs = [p for p in psutil.process_iter(["name", "cpu_percent", "memory_info"])
                     if p.info["name"].lower() == PROCESS_NAME.lower()]

            for p in procs:
                try:
                    total_cpu += p.cpu_percent(interval=None)
                    total_mem += p.memory_info().rss / (1024*1024)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            writer.writerow([timestamp, total_cpu, total_mem])
            f.flush()
            print(f"{time.strftime('%H:%M:%S')} CPU: {total_cpu:.1f}%, MEM: {total_mem:.1f} MB")
            time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor()
