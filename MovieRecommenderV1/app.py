# app.py
from flask import Flask, render_template, request
from reddis_client import r
from recommender import recommend
import csv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        person = request.form["person"]
        movie = request.form["movie"]
        rating = request.form["rating"]

        r.hset(f"ratings:{person}", movie, rating)

    people = []
    ratings = {}

    for key in r.keys("ratings:*"):
        name = key.replace("ratings:", "")
        people.append(name)
        ratings[name] = {
            movie_id: int(score)
            for movie_id, score in r.hgetall(key).items()
        }

    return render_template(
        "index.html",
        people=people,
        movies=MOVIES,
        ratings=ratings
    )


def load_movies():
    movies = {}
    with open("data/movies.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["movie_id"]] = row["title"]
    return movies

MOVIES = load_movies()

@app.route("/recommend/<person>")
def recommendations(person):
    ratings_dict = {
        key.replace("ratings:", ""): {
            k: float(v) for k, v in r.hgetall(key).items()
        }
        for key in r.keys("ratings:*")
    }

    recs = recommend(person, ratings_dict)

    return render_template(
        "recommendations.html",
        recs=recs,
        movies=MOVIES
    )


@app.route("/api/rate", methods=["POST"])
def api_rate():
    data = request.json
    r.hset(
        f"ratings:{data['username']}",
        data["movie_id"],
        data["rating"]
    )
    return {"status": "ok"}

@app.route("/api/recommend/<username>")
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
    app.run(debug=True)
