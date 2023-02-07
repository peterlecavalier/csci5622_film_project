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

# Load in the English ids
with open('./data/english_ids.txt', 'r', encoding="utf-8") as f:
    english = f.read()
# Turn into a list
english_ids = english.split(',')
english_ids = [int(i) for i in english_ids]

print(f"There are {len(english_ids)} previously predicted English movies.")

# Set up a rate limiter so we don't overload the API
rate_limiter = RateLimiter(max_calls=100, period=10.0)

movies_data = {}

# Loop over all English movie IDs
for idx, entry in tqdm(enumerate(english_ids)):
    with rate_limiter:
        # Make the API call
        content = requests.get(f"https://api.themoviedb.org/3/movie/{entry}?api_key={api_key}&language=en-US")
        movies_data[entry] = content.json()
        # Store all retrieved data every 2000 calls
        if idx % 2000 == 0:
            with open("./data/all_movies_data.json", "w") as f:
                json.dump(movies_data, f)

# Save the final file
with open("./data/all_movies_data.json", "w") as f:
    json.dump(movies_data, f)