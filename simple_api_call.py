import requests

api_f = open('./api_key.txt', 'r')
api_key = api_f.read()
content = requests.get(
    f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US")
print(content.json())