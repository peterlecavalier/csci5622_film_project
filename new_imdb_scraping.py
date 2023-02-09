import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

df = pd.read_csv('./data/initial_cleaned_data.csv', index_col=0)
imdb_ids = list(df['imdb_id'])

imdb_data = {}

# These headers help with the requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

for idx, id in enumerate(tqdm(imdb_ids)):
    if not pd.isna(id):
        imdb_data[id] = {}
        imdb_page = requests.get(f'https://www.imdb.com/title/{id}/', headers=headers)
        if not imdb_page.ok:
            print(f"{id} failed")
        try:
            soup = BeautifulSoup(imdb_page.text, "html.parser")
            rating_div = soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            budget_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-budget'})
            rev_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            if rating_div is not None:
                imdb_data[id]['imdb_rating'] = rating_div.contents[0].contents[0]
            if budget_li is not None:
                imdb_data[id]['imdb_budget'] = budget_li.find('label').contents[0]
            if rev_li is not None:
                imdb_data[id]['imdb_revenue'] = rev_li.find('label').contents[0]
        except:
            pass
    if idx % 2000 == 0:
        with open("./data/imdb_data.json", "w") as f:
            json.dump(imdb_data, f)
# Save the final file
with open("./data/imdb_data.json", "w") as f:
    json.dump(imdb_data, f)