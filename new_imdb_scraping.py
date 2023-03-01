import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from tqdm.contrib.concurrent import process_map
#from p_tqdm import p_map
import time

def pull_imdb(id):
    rating = ""
    budget = ""
    revenue = ""

    # These headers help with the requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    if not pd.isna(id):
        imdb_page = False
        for attempt in range(5):
            try:
                imdb_page = requests.get(f'https://www.imdb.com/title/{id}/', headers=headers)
                break
            except:
                time.sleep(3)
        if not imdb_page.ok:
            print(f"{id} failed")
        try:
            soup = BeautifulSoup(imdb_page.text, "html.parser")
            rating_div = soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            budget_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-budget'})
            rev_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            if rating_div is not None:
                rating = rating_div.contents[0].contents[0]
            if budget_li is not None:
                budget = budget_li.find('label').contents[0]
            if rev_li is not None:
                revenue = rev_li.find('label').contents[0]
        except:
            pass

        imdb_data = f"{id}&{rating}&{budget}&{revenue}"
        return imdb_data

def test_func(id):
    time.sleep(1)
    return id


if __name__ == '__main__':
    df = pd.read_csv('./data/post_vis_cleaned_data.csv', index_col=0)
    imdb_ids = list(df['imdb_id'])
    final_list = process_map(pull_imdb, imdb_ids, chunksize=100, max_workers=6)

    save_dict = {}
    for i in final_list:
        if i is not None:
            try:
                items = i.split('&')
                id = items[0]
                rating = items[1]
                budget = items[2]
                revenue = items[3]
                save_dict[id] = {'rating': rating, 'budget': budget, 'revenue': revenue}
            except:
                print(f"Couldn't save {i}")

    # Save the final file
    with open("./data/imdb_data.json", "w") as f:
        json.dump(save_dict, f)
