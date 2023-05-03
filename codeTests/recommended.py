import omdb
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#everything for OMDB
OMDB_API_KEY = "6c9bb17f&t="
OMDB_LINK = "https://omdbapi.com/?apikey="

# Prompt user for movie title
title = input("Enter a movie title: ")

# Send request to API with title and key
response = requests.get(OMDB_LINK + OMDB_API_KEY, params={'t': title, 'plot': 'full'})

# Extract information about the movie
if response.status_code == 200:
    data = response.json()

    # Extract plot summary from response
    plot_summary = data.get('Plot', '')

    # Search for movies similar to the input movie based on plot summary
    response = requests.get(OMDB_LINK + OMDB_API_KEY, params={'s': title, 'type': 'movie'})
    data = response.json()
    search_results = data.get('Search', [])

    # Extract plot summaries from search results
    plot_summaries = [result.get('Plot', '') for result in search_results]

    # Combine input plot summary with plot summaries from search results
    all_plot_summaries = [plot_summary] + plot_summaries

    # Vectorize plot summaries using TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    plot_summary_vectors = vectorizer.fit_transform(all_plot_summaries)

    # Calculate cosine similarity between input movie and search results
    cosine_similarities = cosine_similarity(plot_summary_vectors[0], plot_summary_vectors[1:])

    # Get indices of top 5 most similar movies
    top_indices = cosine_similarities.argsort()[0][-5:]

    # Print recommended movies
    print('Recommended movies:')
    for i in reversed(top_indices):
        print(search_results[i]['Title'])
        print(search_results[i]['Year'])

else:
    print(f"Error: {response.status_code}")