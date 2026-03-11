import pandas as pd
from recommender import build_matrix, recommend

def test_build_matrix():
    ratings = {
        "alice": {"1": 5, "2": 3},
        "bob": {"1": 4}
    }

    matrix = build_matrix(ratings)

    assert isinstance(matrix, pd.DataFrame)
    assert matrix.loc["alice", "1"] == 5
    assert matrix.loc["bob", "2"] == 0

def test_recommend_known_user():
    ratings = {
        "alice": {"1": 5, "2": 3},
        "bob": {"1": 4, "3": 2}
    }

    recs = recommend("alice", ratings, top_n=2)

    assert len(recs) <= 2
    assert isinstance(recs.index, pd.Index)

def test_recommend_unknown_user():
    ratings = {"bob": {"1": 4}}
    recs = recommend("alice", ratings)
    assert recs == []