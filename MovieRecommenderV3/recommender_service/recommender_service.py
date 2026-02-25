from flask import request, Flask

from recommender import recommend
from shared.redis_client import r

app = Flask(__name__)

@app.route("/api/recommend/<username>", methods=["GET"])
def api_recommend(username):
    ratings_dict = {
        key.replace("ratings:", ""): {
            k: float(v) for k, v in r.hgetall(key).items()
        }
        for key in r.keys("ratings:*")
    }
    recs = recommend(username, ratings_dict)
    return recs.to_dict() if recs is not None else {}

if __name__ == "__main__":
    print("Recommendation service starting on port 5001 …")
    app.run(host="0.0.0.0",port=5001)