import csv
import time
import threading
import requests
from collections import defaultdict

APP_URL = "http://127.0.0.1:5000"

MOVIE_MAP = {}

with open("data/movies.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, quotechar='"')
    for row in reader:
        MOVIE_MAP[row["title"]] = row["movie_id"]

print("Loaded movies:", MOVIE_MAP)

def user_worker(username, actions):
    count = 0

    for movie, rating in actions:
        payload = {
            "username": username,
            "movie_id": MOVIE_MAP[movie],
            "rating": rating
        }

        requests.post(f"{APP_URL}/api/rate", json=payload)
        count += 1

        if count % 3 == 0:
            requests.get(f"{APP_URL}/api/recommend/{username}")

        time.sleep(0.5)  # simulate human delay

def run_workload(csv_file):
    actions = defaultdict(list)

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            actions[row["username"]].append(
                (row["movie_title"], int(row["rating"]))
            )

    threads = []
    for user, acts in actions.items():
        t = threading.Thread(target=user_worker, args=(user, acts))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # signal the monitor to stop
    with open("STOP_MONITORING", "w") as f:
        f.write("done")


if __name__ == "__main__":
    run_workload("data/ratings_workload.csv")
