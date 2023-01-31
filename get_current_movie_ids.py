import requests
from datetime import datetime, timedelta
import os

# Get the current date/time
now = datetime.utcnow()

# Data is uploaded by 8:00 AM UTC as per TMDB documentation
if now.hour < 8:
    now = now - timedelta(days = 1)
month = f"{now.month:02d}"
day = f"{now.day:02d}"
year = f"{now.year}"

# This is the most current list of movies on their entire database
index_fname = f"movie_ids_{month}_{day}_{year}.json.gz"
index_url = "http://files.tmdb.org/p/exports/" + index_fname

save_path = os.path.abspath("./data/" + index_fname)

if not os.path.isfile(save_path):
    # This gets the data for us
    index_response = requests.get(index_url, allow_redirects=True)

    # Save the data locally
    open(save_path, 'wb').write(index_response.content)
else:
    print(f"Most current data already saved at {save_path}.")