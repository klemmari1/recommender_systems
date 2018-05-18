# -*- encoding: utf8 -*-
import collaborative_filtering
import content_based_filtering
import operator


def main(number_of_recommendations=3):
    content_ratings = content_based_filtering.main(0)
    collaborative_ratings = collaborative_filtering.main()
    movie_data = content_based_filtering.loadData('movies.csv')
    content_weight = 0.3
    collaborative_weight = 0.7
    scores = {}
    for user, ratings in content_ratings.items():
        if(user not in scores):
            scores[user] = {}
        #Calculate the score according to the weightings
        for movie, content_score in ratings.items():
            if (movie in collaborative_ratings[user]):
                scores[user][movie] = content_weight * content_score + collaborative_weight * collaborative_ratings[user][movie]
        scores[user] = dict(sorted(scores[user].items(), key=operator.itemgetter(1), reverse=True))
    for user, movies in scores.items():
        print("Scores for user " + str(user) + ":")
        for idx, movie in enumerate(movies):
            print(movie_data[movie_data.movieId == movie].title.item() + ": " + str(movies[movie]))
            if idx >= number_of_recommendations-1:
                break


if __name__ == '__main__':
    main()
