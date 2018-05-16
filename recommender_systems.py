from math import sqrt, pow
import pandas as pd
import operator
 
def loadData(csv):
    data = pd.read_csv('ml-latest-small/' + csv, quotechar='"')
    return data
 
def user_sim_cosine_sim(dataset1, dataset2):
# computes similarity between two users based on the cosine similarity metric
    numerator = 0
    for key, _ in dataset1.items():
        if (key in dataset2):
            numerator += float(dataset1[key]) * float(dataset2[key])
    A = 0
    B = 0
    for _, value in dataset1.items():
        A += pow(float(value), 2.0)
    for _, value in dataset2.items():
        B += pow(float(value), 2.0)
    denominator = sqrt(A) * sqrt(B)
    return numerator / denominator

def most_similar_movies(genre_dict, movie_dict, number_of_movies):
# returns top-K similar users for the given user
    movies = {}
    for movie, movie_genres in movie_dict.items():
        movies[movie] = user_sim_cosine_sim(genre_dict, movie_genres)
    sorted_movies = sorted(movies, key=movies.get, reverse=True)
    best_movies = {}
    for idx, movie in enumerate(sorted_movies):
        best_movies[movie_data[movie_data.movieId == movie].title.item()] = movies[movie]
        if idx == number_of_movies:
            break
    return best_movies

def user_recommendations(genre_dict, movie_dict, movie_data, seen_movies):
# generate recommendations for the given user
    number_of_movies = 5
    best_movies = most_similar_movies(genre_dict, movie_dict, number_of_movies)
    return best_movies


rating_data = loadData('ratings.csv')
movie_data = loadData('movies.csv')

user_genres = {}
seen_movies = {}
keys = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
        "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
        "Romance", "Sci-Fi", "Thriller", "War", "Western"]
for index, row in rating_data.iterrows():
    if (row.userId not in seen_movies):
        seen_movies[row.userId] = []
    seen_movies[row.userId].append(row.movieId)
    if (row.userId not in user_genres):
        user_genres[row.userId] = {key: 0 for key in keys}
    if (row.movieId >= 2.5):
        movie_row = movie_data[movie_data.movieId == row.movieId]
        genres = movie_row.genres.item().split("|")
        for genre in genres:
            if (genre in keys):
                user_genres[row.userId][genre] += 1

movie_dict = {}
for index, row in movie_data.iterrows():
    if (row.genres != "(no genres listed)"):
        movie_dict[row.movieId] = {}
        genres = row.genres.split("|")
        for genre in genres:
            if (genre in keys):
                movie_dict[row.movieId][genre] = 1

for user, genre_dict in user_genres.items():
    print("Recommended movies for user " + str(user) + ":")
    print(user_recommendations(genre_dict, movie_dict, movie_data, seen_movies))
