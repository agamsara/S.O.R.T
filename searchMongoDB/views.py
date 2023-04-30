import re
# django loads up shortcuts
from django.shortcuts import render

# from django.http import HttpResponse
import datetime

#for mongoDB
import pymongo

#for imdb: https://cinemagoer.github.io/
from imdb import Cinemagoer

#for url import
import requests

from django.shortcuts import render
from home.models import SearchQuery
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Q
from home.models import SearchQuery, SearchResult,SearchHistory

# This is the HTML file called when the logic finishes
SEARCH_RESULTS_DIRECTORY = "searchMongoDBTemplates/events/search_results.html"

# This is the MongoDB connection string, its currently using my (Connor Puckett) log in credentials, probably need to obfuscate somehow
CONNECTION_STRING = "mongodb+srv://Con-Rez:KVc5QUF3bZdic8ig@academyawardscluster.kghzx33.mongodb.net/?retryWrites=true&w=majority"

#These are the databases accessed. Currently set to master since we aren't editing anything
ACADEMY_DATABASE_USED = 'AcademyAwardsDocuments'
ACADEMY_COLLECTION_USED = 'AcademyAwardsMaster'

OSCAR_DATABASE_USED = 'OscarAwardsDocuments'
OSCAR_COLLECTION_USED = 'OscarAwardsMaster'

#TO DO: Need to check if the professor wanted the year the film was released or the year the ceremony happened
SEARCH_YEAR_TYPE = "year_film"

#Everything for OMDB
OMDB_API_KEY = "6c9bb17f&t="
OMDB_LINK = "https://omdbapi.com/?apikey="

# Create your views here.
def index(request):
    #This can override the HTML file in its entirety!
    #return HttpResponse("Hello world, this is a python file output!")
    today = datetime.datetime.now().date() 
    return render(request,"searchMongoDBTemplates/searchPage.html", {"today": today})

def search_results(request):
    
    # If input was not blank
    if request.method == "POST":
        # Run code here for search return of values
        # get search input from search bar
        val = request.POST['searchInputFromNavbar']

        # get filter parameters from request
        category_filter = request.POST.get('categoryFilter')
        award_type_filter = request.POST.get('awardTypeFilter')
        

        # Check input
        if re.match(r'^\d{4}$', val) and 1926 <= int(val) <= 2025:
            # Attempt MongoDB Connection
            while True:
                print("Initializing Database ", ACADEMY_DATABASE_USED, " and it's Collection ", ACADEMY_COLLECTION_USED, "...")
                # Display warning in console
                print(
                    "Connction String created from hardcoded entry from Con-Rez's account. It would be better to prompt for a username and password here instead of doing this.\n")
                try:
                    client = pymongo.MongoClient(CONNECTION_STRING)  # Connect to MongoDB, create a MongoClient
                    database_name = client[ACADEMY_DATABASE_USED]  # Access database
                    collection_name = database_name[
                        ACADEMY_COLLECTION_USED]  # Access Collection within database
                    print("Connected successfully!!!\n")
                    break
                except:
                    print("Could not connect to MongoDB, retrying...\n")

            # first get the academy awards winners
            # list to record results to
            # next, make list for oscars using the year as well
            print("Making Lists for oscars...")
            nameListToSend = []
            categoryListToSend = []
            winnerListToSend = []
            filmListToSend = []
            mongoDB_IDListToSend = []
            moviePosterListToSend = []

            # database_name = client[OSCAR_DATABASE_USED]  # Access database
            # collection_name = database_name[OSCAR_COLLECTION_USED]  # Access Collection within database
            # Record each entry that applies to search to the list
            try:
                print("Searching for a document")
                # attempt finding at least one
                if collection_name.find_one({SEARCH_YEAR_TYPE: int(val)}):
                    print("Beginning record to list")
                    # when a document is found, record it and the rest of the matching documents to a list
                    for eachEntry in collection_name.find({SEARCH_YEAR_TYPE: int(val)}):
                        # TO DO: Whomever added the commented out if statements did NOT leave comments as to what they were for. So I removed them.
                            #if (eachEntry['winner'] == "True" and (eachEntry['category'] == "BEST PICTURE" or eachEntry['category'] == "OUTSTANDING PICTURE")):  # If the entry was a winner of either best or outstanding picture
                                # if not category_filter or eachEntry['category'].lower() == category_filter.lower():
                                    # if not award_type_filter or eachEntry['award_type'].lower() == award_type_filter.lower():
                        
                        #add each point of data to list
                        nameListToSend.append(eachEntry['name'])
                        categoryListToSend.append(eachEntry['category'].title().replace('Best', "")) # Add entry, if category starts with word Best, remove it for formatting consistency
                        if (eachEntry['winner'] == "True"):     #If they were a winner, then they Won
                            winnerListToSend.append("Won")
                        elif (eachEntry['winner'] == "False"):  #If they were not a winner, then they were nominated
                            winnerListToSend.append("Nominated")
                        filmListToSend.append(eachEntry['film'])
                        mongoDB_IDListToSend.append(eachEntry['_id'])
                        
                        print("Entry recorded.")
                # else there is not one to find
                else:
                    return render(request, SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Match not found."})
            except:
                return render(request, SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Search failure. The code is likely bugged."})

            # Compress lists to one variable and send to html
            print("Sending list to display.\n")
            masterList = zip(nameListToSend, categoryListToSend, winnerListToSend, filmListToSend, mongoDB_IDListToSend)
            return render(request, SEARCH_RESULTS_DIRECTORY, {'searched': val, 'listToDisplay': masterList})
        
        # Perhaps val is actually a movie title
        else:
            try:
                response = requests.get(OMDB_LINK + OMDB_API_KEY + val)

                if response.json()['Response'] == "True":
                    print("Title: " + response.json()['Title'])
                    print("Poster Art: " + response.json()['Poster'])
                    print("Year: " + response.json()['Year'])
                    print("Director: " + response.json()['Director'])
                    print("Language: " + response.json()['Language'])
                    return render(request, SEARCH_RESULTS_DIRECTORY,
                                  {'Title': response.json()['Title'], 
                                   'Poster': response.json()['Poster'], 
                                   'Year': response.json()['Year'],
                                   'Director': response.json()['Director'], 
                                   'Language': response.json()['Language']})
                else:
                    print("Movie not found!")
                    return render(request, SEARCH_RESULTS_DIRECTORY,
                                  {'errorReport': "The value has no matches. Make sure to enter either a movie name or year."})
            # or its not anything
            except:
                return render(request, SEARCH_RESULTS_DIRECTORY,
                              {'errorReport': "ERROR: The value has no known matches or interpretations."})
    # if field blank
    else:
        return render(request, SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: The search bar was blank."})

    
def search(request):
    # Get the user's search query from the request
    query = request.GET.get('q')

    # Save the search query to the database
    if query:
        search_query = SearchQuery(user=request.user, query=query)
        search_query.save()

        # Save the search query to the user's search history
        history_item = SearchHistory(user=request.user, query=query)
        history_item.save()

    # Perform the search
    results = SearchResult.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    # Render the search results template with the search results
    return render(request, 'search_results.html', {'results': results})    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login credentials'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('home')

     
def history_view(request):
    if request.user.is_authenticated:
        history_items = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'history.html', {'history_items': history_items})
    else:
        return redirect('login')
    
def save_search(query):
    search = SearchHistory(query=query)
    search.save()
    
def get_search_history():
    searches = SearchHistory.objects.order_by('-timestamp')
    return searches