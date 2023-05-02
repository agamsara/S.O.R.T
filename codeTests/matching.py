#for imdb: https://cinemagoer.github.io/
from imdb import Cinemagoer
 

#for omdb
import requests 
import json


#Everything for OMDB
OMDB_API_KEY = "6c9bb17f&t="
OMDB_LINK = "https://omdbapi.com/?apikey="

# Replace MOVIE_TITLE with the title of the movie you want to search for
movie_title = 'Water'

# Make a request to the OMDb API to get information about the movie
movie_url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}&plot=full'
response = requests.get(movie_url)
movie_data = json.loads(response.text)

# Print information about the movie
print(f'Title: {movie_data["Title"]}')
print(f'Year: {movie_data["Year"]}')
print(f'Director: {movie_data["Director"]}')
print(f'Actors: {movie_data["Actors"]}')
print(f'Plot: {movie_data["Plot"]}')

# Use the title of the movie to search for related movies
related_movies_url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_data["Title"]}&type=movie'
response = requests.get(related_movies_url)
related_movies_data = json.loads(response.text)

# Print information about the related movies
if 'Search' in related_movies_data:
    related_movies = related_movies_data['Search'][1:7]
    related_imdb_ids = []
    num_related_movies = len(related_movies)
    
    if num_related_movies > 1:
        print('Related movies:')
        for related_movie in related_movies:
            if related_movie['imdbID'] in related_imdb_ids:
                continue
            
            related_imdb_ids.append(related_movie['imdbID'])
            
            print(f'Title: {related_movie["Title"]}')
            print(f'Year: {related_movie["Year"]}')
            print(f'Poster URL: {related_movie["Poster"]}')
            print()
    else:
        print('No related movies found.')
else:
    print('No related movies found.')