from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import requests
import json

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://OleksandrK:{password}@academyawardscluster.kghzx33.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

oscarDB = client.OscarAwardsDocuments
oscarDBcollection =  oscarDB.OscarAwardsMaster

apiKey = "6c9bb17f&t="
link = "https://omdbapi.com/?apikey="

printer = pprint.PrettyPrinter()


year = 2012 # year to find best actor

def find_BestActorsByYear(year, apiKey, link):
    bestActor = oscarDBcollection.find_one({"year_ceremony": year, "category": "ACTOR IN A LEADING ROLE", "winner": "True"}) #search in MongoDB/ AcademyAwardsMaster for Best Actor
    title= bestActor["film"] 

    response = requests.get(link + apiKey + title) # API request to get info from OMDB
    printer.pprint(bestActor) # prints from MongoDB/ AcademyAwardsMaster
    printer.pprint(response.json()) # prints from OMDB 



find_BestActorsByYear(year, apiKey, link)

