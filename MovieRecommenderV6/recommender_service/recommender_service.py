import time
from flask import request, Flask, jsonify
from recommender import recommend
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

@app.route("/api/recommend/<username>", methods=["GET"])
def api_recommend(username):
    start_time = time.time()
    try:
        ratings_dict = {
            key.replace("ratings:", ""): {
                k: float(v) for k, v in r.hgetall(key).items()
            }
            for key in r.keys("ratings:*")
        }
        recs = recommend(username, ratings_dict)
        response = jsonify(recs.to_dict() if recs is not None else {})
        status_code = response.status_code
        return response

    except Exception as e:
        status = "500"
        raise e

    finally:
        latency = time.time() - start_time
        REQUEST_COUNT.labels(request.method, endpoint="/api/recommend", status=status).inc()
        REQUEST_LATENCY.labels(request.method, endpoint="/api/recommend",).observe(latency)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    print("Recommendation service starting on port 5001 …")
    app.run(host="0.0.0.0",port=5001)