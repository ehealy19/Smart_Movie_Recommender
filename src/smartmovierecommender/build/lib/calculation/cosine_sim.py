import numpy as np
import pandas as pd
from numpy.linalg import norm
import argparse

# MAKING ALL VARIABLES NUMERIC
def convert_duration(duration):
    hours, minutes = 0, 0
    if 'h' in duration:
        hours = int(duration.split('h')[0])
        duration = duration.split('h')[1]
    if 'm' in duration:
        minutes = int(duration.split('m')[0])
    return hours * 60 + minutes

# converting number of ratings to numeric
def convert_ratings(ratings):
    if pd.isna(ratings) or ratings.lower() == 'nan':
        return 0
    if 'K' in ratings:
        return int(float(ratings.replace('K', '')) * 1000)
    if 'M' in ratings:
        return int(float(ratings.replace('M', '')) * 1000000)
    return int(ratings)

def cosine_sim(movie1, movie2):
    """takes in two movies in the form of numpy array and returns the cosine similarity score"""
    movie1 = movie1.flatten()
    movie2 = movie2.flatten()
    cosine = np.dot(movie1,movie2)/(norm(movie1)*norm(movie2))
    print("Cosine Similarity:", cosine)
    
def cosine_max(movie_index, movies):
    movie = movies.iloc[movie_index:movie_index+1].drop(columns=['Title']).to_numpy().flatten()
    similarities = []
        
    for i in range(len(movies)):
        if i != movie_index:
            other_movie = movies.iloc[i:i+1].drop(columns=['Title']).to_numpy().flatten()
            cosine = np.dot(movie, other_movie) / (norm(movie) * norm(other_movie))
            similarities.append((i, cosine))
        
    similarities.sort(key=lambda x: x[1], reverse=True)
    titles = convert_to_title(similarities[:5])
    print(titles)
    return similarities[:5]

def convert_to_title(sims, movies):
    titles = []
    for index, _ in sims:
        titles.append(movies.iloc[index]['Title'])
    return titles