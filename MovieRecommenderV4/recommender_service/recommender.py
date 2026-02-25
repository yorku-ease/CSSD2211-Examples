# recommender.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def build_matrix(ratings_dict):
    df = pd.DataFrame(ratings_dict).T
    return df.fillna(0)

def recommend(target_user, ratings_dict, top_n=5):
    matrix = build_matrix(ratings_dict)

    if target_user not in matrix.index:
        return []

    similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(
        similarity,
        index=matrix.index,
        columns=matrix.index
    )

    weights = sim_df[target_user]
    scores = matrix.T.dot(weights) / weights.sum()

    already_rated = matrix.loc[target_user] > 0
    scores = scores[~already_rated]

    return scores.sort_values(ascending=False).head(top_n)
