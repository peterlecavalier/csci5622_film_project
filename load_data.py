import json

f = open('./data/all_movies_data.json')
all_movies = json.load(f)
keys = list(all_movies.keys())
print(all_movies[keys[1]])