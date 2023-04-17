# django loads up shortcuts
from django.shortcuts import render

# from django.http import HttpResponse
import datetime

#for mongoDB
import pymongo

#for imdb: https://cinemagoer.github.io/
from imdb import Cinemagoer

#for omdb
import requests
import json

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
    #If input was not blank
    if request.method == "POST":
        #Run code here for search return of values
        # get search input from search bar
        val = request.POST['searchInputFromNavbar']

#TO DO: As much as this implementation works, movies named after years or numbers like "2012" and "9" don't work under this logic. We'll need to find a way to confirm the type the person is searching
        # Check input
        try:
            if (1926 < int(val) < 2025):
        # Attempt MongoDB Connection
                while True:
                    print ("Initializing Database ",ACADEMY_DATABASE_USED," and it's Collection ",ACADEMY_COLLECTION_USED ,"...")
                     # Display warning in console
                    print ("Connction String created from hardcoded entry from Con-Rez's account. It would be better to prompt for a username and password here instead of doing this.\n")
                    try:
                        client = pymongo.MongoClient(CONNECTION_STRING) # Connect to MongoDB, create a MongoClient
                        database_name = client[ACADEMY_DATABASE_USED] # Access database
                        collection_name = database_name[ACADEMY_COLLECTION_USED] # Access Collection within database
                        print("Connected successfully!!!\n")
                        break
                    except:  
                        print("Could not connect to MongoDB, retrying...\n")

        #first get the academy awards winners
                # list to record results to
                print("Making List for Academy...")
                academySearchResultsList = []
                # Record each entry that applies to search to the list
                try:
                    print("Searching for a document")
                    #attempt finding at least one
                    if collection_name.find_one({SEARCH_YEAR_TYPE: int(val)}):
                        print("Beginning record to list")
                        # when a document is found, record it and the rest of the matching documents to a list
                        for eachEntry in collection_name.find({SEARCH_YEAR_TYPE: int(val)}):
                            if (eachEntry['winner'] == "True"): # If the entry was a Academy Award Winner
                                academySearchResultsList.append(f"{eachEntry['name']} won the award for \"Best {eachEntry['category'].capitalize()}\" for their role in \"{eachEntry['film']}\"")
                                print("Entry recorded.")
                            else: # If they were not an award winner
                                academySearchResultsList.append(f"{eachEntry['name']} was nominated for the award \"Best {eachEntry['category'].capitalize()}\" for their role in \"{eachEntry['film']}\"")
                                print("Entry recorded.")
                    #else there is not one to find
                    else:
                        return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Match not found."})
                except:
                    return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Search failure. The code is likely bugged."})
                
        # next, make list for oscars using the year as well
                print("Making Lists for oscars...")
                oscarSearchResultsList = []
                database_name = client[OSCAR_DATABASE_USED] # Access database
                collection_name = database_name[OSCAR_COLLECTION_USED] # Access Collection within database
                # Record each entry that applies to search to the list
                try:
                    print("Searching for a document")
                    #attempt finding at least one
                    if collection_name.find_one({SEARCH_YEAR_TYPE: int(val)}):
                        print("Beginning record to list")
                        # when a document is found, record it and the rest of the matching documents to a list
                        for eachEntry in collection_name.find({SEARCH_YEAR_TYPE: int(val)}):
                            if (eachEntry['winner'] == "True" and (eachEntry['category'] == "BEST PICTURE" or eachEntry['category'] == "OUTSTANDING PICTURE")): # If the entry was a winner of either best or outstanding picture
                                oscarSearchResultsList.append(f"{eachEntry['name']} won the award for \"{eachEntry['category'].capitalize()}\" for their role in \"{eachEntry['film']}\"")
                                print("Entry recorded.")
                            elif (eachEntry['winner'] == "True" and (eachEntry['category'] == "ACTOR" or eachEntry['category'] == "ACTRESS")): # If the entry was a winner of best actor
                                oscarSearchResultsList.append(f"{eachEntry['name']} won the award for \"Best {eachEntry['category'].capitalize()}\" for their role in \"{eachEntry['film']}\"")
                                print("Entry recorded.")
                            
                    #else there is not one to find
                    else:
                        return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Match not found."})
                except:
                    return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Search failure. The code is likely bugged."})

                # sent and display html file using input
                print ("Sending list to display.\n")
                return render(request,SEARCH_RESULTS_DIRECTORY, {'searched':val, 'academyResultsList':academySearchResultsList, 'oscarResultsList': oscarSearchResultsList})
            else:
                return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: Enter a valid year, you entered one outside the scope"})
            
        # If not a valid year, then it may be a film name!
        except:
            try:
                #Perhaps val is actually a movie title
                
                response = requests.get(OMDB_LINK + OMDB_API_KEY + val)

                if response.json()['Response'] =="True":
                    print("Title: " + response.json()['Title'])
                    print("Year: " + response.json()['Year'])
                    print("Director: " + response.json()['Director'])
                    print("Language: " + response.json()['Language'])
                    return render(request,SEARCH_RESULTS_DIRECTORY, {'Title': response.json()['Title'], 'Year' : response.json()['Year'], 'Director' : response.json()['Director'], 'Language': response.json()['Language']})
                else:
                    print("Movie not found!")
                    return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "The value has no matches. Make sure to enter either a movie name or year."})
            #or its not anything
            except:
                return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: The value has no known matches or interpretations."})
    #if field blank
    else:
        return render(request,SEARCH_RESULTS_DIRECTORY, {'errorReport': "ERROR: The search bar was blank."})