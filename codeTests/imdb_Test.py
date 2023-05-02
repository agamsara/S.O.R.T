#for imdb: https://cinemagoer.github.io/
from imdb import Cinemagoer

#for omdb
import requests
import json

#Everything for OMDB
OMDB_API_KEY = "6c9bb17f&t="
OMDB_LINK = "https://omdbapi.com/?apikey="

moviePosterListToSend = ''

#IMDB Movie posters
# imdbIndex = Cinemagoer().search_movie('Shrek')
moviePosterListToSend = Cinemagoer().search_movie("Shrek")[0].data["cover url"]
print(moviePosterListToSend)
moviePosterListToSend = Cinemagoer().search_movie('Shrek 2')[0].data["cover url"]
print(moviePosterListToSend)

#OMDB Movie posters
response = requests.get(OMDB_LINK + OMDB_API_KEY + "Shrek")
if response.json()['Response'] == "True":
    print("Title: " + response.json()['Poster'])