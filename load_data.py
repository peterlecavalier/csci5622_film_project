import json

f = open('./data/all_movies_data.json')
    
all_movies = json.load(f)

keys = list(all_movies.keys())

print(len(keys))

#for i in range(10):
#    print(all_movies[keys[i]])