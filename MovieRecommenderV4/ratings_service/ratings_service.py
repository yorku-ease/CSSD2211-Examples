from flask import request, Flask
from shared.redis_client import r

app = Flask(__name__)

@app.route("/api/rate", methods=["POST"])
def api_rate():
    data = request.json
    r.hset(
        f"ratings:{data['username']}",
        data["movie_id"],
        data["rating"]
    )
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)