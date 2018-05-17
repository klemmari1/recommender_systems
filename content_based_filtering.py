# -*- encoding: utf8 -*-

from math import sqrt, pow
import pandas as pd
import operator
 
def loadData(csv):
    data = pd.read_csv('ml-latest-small/' + csv, quotechar='"')
    return data
 
def genre_sim_cosine_sim(user_genres, movie_genres):
# computes similarity between user preferred genres and movie genres based on the cosine similarity metric
    numerator = 0
    for key, _ in user_genres.items():
        if (key in movie_genres):
            numerator += float(user_genres[key]) * float(movie_genres[key])
    A = 0
    B = 0
    for _, value in user_genres.items():
        A += pow(float(value), 2.0)
    for _, value in movie_genres.items():
        B += pow(float(value), 2.0)
    denominator = sqrt(A) * sqrt(B)
    return numerator / denominator

def most_similar_movies(genre_dict, movie_dict, seen_movies, number_of_movies):
# returns top-K best fit movies for the user according to genres
    movies = {}
    for movie, movie_genres in movie_dict.items():
        if(movie not in seen_movies):
            movies[movie] = genre_sim_cosine_sim(genre_dict, movie_genres)
    sorted_movies = sorted(movies, key=movies.get, reverse=True)
    best_movies = {}
    for idx, movie in enumerate(sorted_movies):
        best_movies[movie] = movies[movie]
        if (number_of_movies > 0 and idx == number_of_movies):
            break
    return best_movies

def main(number_of_movies = 5):
    rating_data = loadData('ratings.csv')
    movie_data = loadData('movies.csv')

    user_genres = {}
    seen_movies = {}
    keys = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
            "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
            "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    for _, row in rating_data.iterrows():
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
    for _, row in movie_data.iterrows():
        if (row.genres != "(no genres listed)"):
            movie_dict[row.movieId] = {}
            genres = row.genres.split("|")
            for genre in genres:
                if (genre in keys):
                    movie_dict[row.movieId][genre] = 1

    user_recommendations = {}
    for user, genre_dict in user_genres.items():
        user_recommendations[user] = most_similar_movies(genre_dict, movie_dict, seen_movies[user], number_of_movies)
        #print("Content-based recommended movies for user " + str(user) + ":")
        #print(user_recommendations[user])
    return user_recommendations


if __name__ == '__main__':
    print(main())
