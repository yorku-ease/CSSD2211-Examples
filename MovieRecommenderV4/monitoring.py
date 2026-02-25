import subprocess
import csv
import time
import os

INTERVAL = 1
STOP_FILE = "STOP_MONITORING"

# Reset stop file
if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)

def parse_mem(mem_str):
    mem_str = mem_str.strip()
    if "GiB" in mem_str:
        return float(mem_str.replace("GiB", "")) * 1024  # GB → MB
    elif "MiB" in mem_str:
        return float(mem_str.replace("MiB", ""))       # MB → MB
    else:
        return float(mem_str) / (1024*1024)           # fallback if bytes

def monitor():
    with open("metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "container_name", "cpu_percent", "mem_usage_mb", "mem_limit_mb", "mem_percent"])

        while True:
            if os.path.exists(STOP_FILE):
                print("Stop file detected. Exiting monitoring...")
                break

            # Call `docker stats` once, non-streaming
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format",
                 "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"],
                capture_output=True,
                text=True,
            )
            lines = result.stdout.strip().split("\n")
            for line in lines:
                try:
                    name, cpu, mem = line.split(",")
                    cpu = float(cpu.strip("%"))
                    used, limit = mem.split("/")
                    mem_usage_mb = parse_mem(used)
                    mem_limit_mb = parse_mem(limit)
                    mem_percent = (mem_usage_mb / mem_limit_mb) * 100
                    writer.writerow([time.time(), name, cpu, mem_usage_mb, mem_limit_mb, mem_percent])
                    print(f"{name} CPU: {cpu}%, MEM: {mem_usage_mb:.2f}/{mem_limit_mb:.2f} MB ({mem_percent:.1f}%)")
                except Exception as e:
                    continue

            time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor()
