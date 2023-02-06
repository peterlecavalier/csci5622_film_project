import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import math
from tqdm import tqdm

df = pd.read_csv('./data/initial_cleaned_data.csv', index_col=0)
imdb_ids = list(df['imdb_id'])

imdb_ratings = []

# These headers help with the requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

for id in tqdm(imdb_ids[:100]):
    if not pd.isna(id):
        imdb_page = requests.get(f'https://www.imdb.com/title/{id}/', headers=headers)
        if not imdb_page.ok:
            print(f"{id} failed")
        try:
            #print(imdb_page.text)
            soup = BeautifulSoup(imdb_page.text, "html.parser")
            rating_div = soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            if rating_div is not None:
                imdb_ratings.append(float(rating_div.contents[0].contents[0]))
            else:
                imdb_ratings.append(-1.0)
        except:
            imdb_ratings.append(-1.0)
    else:
        imdb_ratings.append(-1.0)



df['imdb_ratings'] = imdb_ratings

df.to_csv('./data/ratings_cleaned_data.csv')
        

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