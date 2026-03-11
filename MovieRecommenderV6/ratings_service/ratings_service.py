import time
from flask import request, Flask
from shared.redis_client import r
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
)


app = Flask(__name__)

@app.route("/api/rate", methods=["POST"])
def api_rate():
    start_time = time.time()
    status = "200"
    try:
        data = request.json
        r.hset(
            f"ratings:{data['username']}",
            data["movie_id"],
            data["rating"]
        )
        return {"status": "ok"}

    except Exception as e:
        status = "500"
        return {"error": "invalid request"}, 500

    finally:
        latency = time.time() - start_time
        REQUEST_COUNT.labels(method=request.method, endpoint="/api/rate", status=status).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint="/api/rate").observe(latency)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)