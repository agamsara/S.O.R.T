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

nomineesDB = client.AcademyAwardsDocuments
nomineesDBcollection =  nomineesDB.AcademyAwardsMaster

oscarDB = client.OscarAwardsDocuments
oscarDBcollection =  oscarDB.OscarAwardsMaster

apiKey = "6c9bb17f&t="
link = "https://omdbapi.com/?apikey="

printer = pprint.PrettyPrinter()


year = 2008 # year to find oscar winners

def find_oscarWinnersByYear(year, apiKey, link):
    oscarWinners = oscarDBcollection.find_one({"year_ceremony": year, "category": "BEST PICTURE", "winner": "True"}) #search in MongoDB/ AcademyAwardsMaster for Oscar winner
    title= oscarWinners["film"] 

    response = requests.get(link + apiKey + title) # API request to get info from OMDB
    printer.pprint(oscarWinners) # prints from MongoDB/ AcademyAwardsMaster
    printer.pprint(response.json()) # prints from OMDB 



find_oscarWinnersByYear(year, apiKey, link)

