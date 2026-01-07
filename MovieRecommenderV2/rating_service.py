from flask import request, Flask
from reddis_client import r

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
    app.run(port=5000)