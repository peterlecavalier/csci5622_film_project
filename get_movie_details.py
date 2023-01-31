import gzip
import glob
import os
import json
import requests
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
from ratelimiter import RateLimiter

api_f = open('./api_key.txt', 'r')
api_key = api_f.read()

# Get the most recent data file
all_files = glob.glob('./data/*.json.gz')
jsonfilename = max(all_files, key=os.path.getctime)

# Inflate the compressed json
with gzip.open(jsonfilename, 'r') as f:
    json_bytes = f.read()

# Decode the json and separate it 
json_full_str = json_bytes.decode('utf-8')
json_sep = json_full_str.split("\n")

# parse the json into list of movies
all_jsons_list = [json.loads(entry) for entry in json_sep if len(entry) != 0]

# Get the movie name for each entry
# also separate index and entry for printing with multiprocessing
movie_names = [i['original_title'] for i in all_jsons_list]

# Load in the English titles
with open('./data/english_names.txt', 'r', encoding="utf-8") as f:
    english = f.read()
# Turn into a list
english_ids = english.split(',')
english_ids = [int(i) for i in english_ids]

print(f"There are {len(english_ids)} previously predicted English movies.")

# Get all the jsons for English titled movies
english_movies = all_jsons_list.copy()[english_ids]

# Set up a rate limiter so we don't overload the API
rate_limiter = RateLimiter(max_calls=40, period=1)

movies_data = {}

for entry in tqdm(english_movies):
    with rate_limiter:
        content = requests.get(f"https://api.themoviedb.org/3/movie/{entry}?api_key={api_key}&language=en-US")
        movies_data[entry] = content.json()

with open("./data/all_movies_data.json", "w") as f:
    json.dump(movies_data, f)



'''
movies_pop = {}
for i in movies:
    if movies[i]['popularity'] > 0:
        movies_pop[i] = movies[i]
print(f"There are {len(movies_pop)} popular movies in total")
'''

"""
shuffle(all_jsons_list)

selected = all_jsons_list[:(len(all_jsons_list) // 100 + 1)]

popularities = [i['vote_average'] for i in all_jsons_list if 'vote_average' in i.keys()]

plt.boxplot(popularities)
plt.show()
"""