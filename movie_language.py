import gzip
import glob
import os
import json
import time
from langdetect import detect
from multiprocessing import Pool

# Detect whether the language is English or not
# Return to the multiprocessing
def language(x):
    print(x[0])
    try:
        detection = detect(x[1])
        if detection == 'en':
            return 'en'
        else:
            return 'no'
    except:
        return 'er'

if __name__ == '__main__':
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
    movie_names = [[idx, i] for idx, i in enumerate(movie_names)]

    english = []
    non_english = []
    errors = []
    start = time.time()
    # Compute the language of each movie title
    with Pool() as pool:
        languages = pool.map(language, movie_names)
    end = time.time()
    print(f"Program finished! Took {end-start}s.")

    # Make a list separating the languages
    for idx, name in enumerate(movie_names):
        if languages[idx] == 'en':
            english.append(name[0])
        elif languages[idx] == 'no':
            non_english.append(name[0])
        else:
            errors.append(name[0])

    english = [str(i) for i in english]
    non_english = [str(i) for i in non_english]
    errors = [str(i) for i in errors]
    
    # Write this to txt files
    with open('./data/english_names.txt', 'w', encoding="utf-8") as f:
        f.write(','.join(english))

    with open('./data/non_english_names.txt', 'w', encoding="utf-8") as f:
        f.write(','.join(non_english))

    with open('./data/error_names.txt', 'w', encoding="utf-8") as f:
        f.write(','.join(errors))