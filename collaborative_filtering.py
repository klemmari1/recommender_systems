# -*- encoding: utf8 -*-

from math import sqrt, pow
from numpy import genfromtxt
import numpy
import operator
 
def loadData():
    data = genfromtxt('ml-latest-small/ratings.csv', delimiter=',', dtype=None, encoding=None)
    return data
 
def user_sim_cosine_sim(person1, person2):
# computes similarity between two users based on the cosine similarity metric
    numerator = 0
    for key, _ in person1.items():
        if (key in person2):
            numerator += float(person1[key]) * float(person2[key])
    A = 0
    B = 0
    for key, value in person1.items():
        A += pow(float(value), 2.0)
    for key, value in person2.items():
        B += pow(float(value), 2.0)
    denominator = sqrt(A) * sqrt(B)
    return numerator / denominator

def user_sim_pearson_corr(person1, person2):
# computes similarity between two users based on the pearson similarity metric
    mean1 = 0
    mean2 = 0
    B1 = 0
    B2 = 0
    for _, value in person1.items():
        mean1 += float(value)
        B1 += pow(float(value), 2.0)
    for _, value in person2.items():
        mean2 += float(value)
        B2 += pow(float(value), 2.0)
    mean1 /= len(person1)
    mean2 /= len(person2)
    A = 0
    for key, value in person1.items():
        if (key in person2):
            A += (float(person1[key]) - mean1) * (float(person2[key]) * mean2)
    B = sqrt(B1) * sqrt(B2)
    return A / B

def most_similar_users(person, number_of_users, data):
# returns top-K similar users for the given user
    users = {}
    for person2, _ in data.items():
        if(person != person2):
            users[person2] = user_sim_cosine_sim(data[person], data[person2])
    sorted_users = sorted(users, key=users.get, reverse=True)
    best_users = {}
    for idx, user in enumerate(sorted_users):
        best_users[user] = users[user]
        if idx == number_of_users:
            break
    return best_users

def user_recommendations(person, data):
# generate recommendations for the given user
    number_of_users = 2
    sim_users = most_similar_users(person, number_of_users, data)
    numerators = {}
    denominators = {}
    for user, score in sim_users.items():
        for movie, rating in data[user].items():
            if movie not in data[person].items():
                if movie not in numerators:
                    numerators[movie] = 0
                if movie not in denominators:
                    denominators[movie] = 0
                numerators[movie] += float(score) * float(rating)
                denominators[movie] += score * 5 # 5 = Max rating for movies. Normalizing scores between 0 and 1.
    ratings = {}
    for movie, _ in numerators.items():
        ratings[movie] = numerators[movie] / denominators[movie]
    sorted_ratings = dict(sorted(ratings.items(), key=operator.itemgetter(1)))
    return sorted_ratings

def main():
    data = loadData()
    data = numpy.delete(data, 0, 0)
    user_dict = {}
    for line in data:
        if (line[0] not in user_dict):
            user_dict[line[0]] = {}
        #Add rating (line[2]) to the user id's (line[0]) dict's movie id (line[1]) entry
        user_dict[line[0]][line[1]] = line[2]
    user_recommnd = {}
    for user, data in user_dict.items():
        user_recommnd[user] = user_recommendations(user, user_dict)
        #print("Collaborative movie ratings for user " + str(user) + ":")
        #print(user_recommendations[user])
    return user_recommnd


if __name__ == '__main__':
    print(main())
