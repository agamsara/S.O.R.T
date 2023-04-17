# Before attempting to run this python file, you must install pymongo. Open the terminal in VSCode using Ctrl+` and type in "pip install pymongo"
import pymongo

# Much of what was gleaned here was found from the following
# How to use Python with MongoDB: https://www.mongodb.com/languages/python#:~:text=Connecting%20Python%20and%20MongoDB%20Atlas%201%20Creating%20a,file%20called%20pymongo_test_insert.pyfile%2C%20add%20the%20following%20code.%20

# This is the MongoDB connection string, its currently using my (Connor Puckett) log in credentials, probably need to obfuscate somehow
CONNECTION_STRING = "mongodb+srv://Con-Rez:KVc5QUF3bZdic8ig@academyawardscluster.kghzx33.mongodb.net/?retryWrites=true&w=majority"

DATABASE_USED = 'AcademyAwardsDocuments'
COLLECTION_USED = "AcademyAwardsMaster"

# Display warning this is for testing only
print ("Connction String created from hardcoded entry from Con-Rez's account. It would be better to prompt for a username and password here instead of doing this.\n")

# Attempt MongoDB Connection
print ("Initializing Database ",DATABASE_USED," and it's Collection ",COLLECTION_USED ,"...")
while True:
    print ("Attempting a connection using the credentials...")
    try:
        client = pymongo.MongoClient(CONNECTION_STRING) # Connect to MongoDB, create a MongoClient
        database_name = client[DATABASE_USED] # Access database
        collection_name = database_name[COLLECTION_USED] # Access Collection within database
        print("Connected successfully!!!\n")
        break
    except:  
        print("Could not connect to MongoDB, retrying...\n")

print
# Use to download kaggle database using API command (might be useful): kaggle datasets download -d unanimad/the-oscar-award

# Get the database for our example
# NOTE: These aren't created if no data is written to them when running this

# Main Menu
while True:
    print ("=== MAIN MENU ===\nType one of the following numbers and hit enter to begin test of MongoDB")
    print ("1 - NOT RECOMMENDED TO USE: Mass Insert hardcoded entries to MongoDB's ",COLLECTION_USED ," Collection.")
    print ("2 - Display all entries in both a not clean and clean way from the ",COLLECTION_USED ," Collection")
    print ("3 - Insert a hardcoded entry into MongoDB's ",COLLECTION_USED ," Collection. Check for a duplicate before doing so.")
    print ("4 - Input a year, search for and return all entries containing that year. ")
    print ("5 - Delete a document based on Year and Actor Name. ")
    print ("8 - ALREADY DONE, CODE INCLUDED FOR REFERENCE: Index the Academy Award Test Collections")
    print ("9 - Exit Program")
    val = input ("> ")

    # Check input
    while val not in ('1', '2', '3', '4', '5', '8', '9'):
        val = input ("Please enter a valid input:\n> ")

    match val:

        # The below will add new, hardcoded entries to the database (but it won't merge and check for duplicates during it!)
        case '1':
            val = input ("Enter 'y' if you would like to INSERT changes to the Academy. Enter 'n' to return to the MAIN MENU.\nNOTE: If an entry already exists, duplicate entries will be made!\n> ")

            # Check input
            while val not in ('y', 'n'):
                val = input ("Please enter a valid input:\n> ")

            match val:
                case 'y':
                    print ("Hooray!")
            
                    #Add these entries
                    item_1 = {
                    "year_film" : 2024,
                    "year_ceremony" : 2024,
                    "ceremony" : 9,
                    "category" : "TEST",
                    "name" : "Connor Puckett",
                    "film" : "Test for MongoDB: A Database Like No Other",
                    "winner" : "False"
                    }

                    item_2 = {
                    "year_film" : 2025,
                    "year_ceremony" : 2025,
                    "ceremony" : 10,
                    "category" : "TEST",
                    "name" : "Ryan Desagun",
                    "film" : "Test for MongoDB Part 2: The Rise of Ainsley",
                    "winner" : "False"
                    }

                    #Apply the changes to the MongoDB Cluster
                    collection_name.insert_many([item_1,item_2])

                case 'n':
                    print ("Boooo!")
                
                # This is in case something horrific happens
                case _:
                    print ("I'm a teapot! How did we get here?!?")

        # This will read all the documents from a Collection in a bad way and a good way
        case '2':
            val = input ("Enter 'y' if you would like to view the documents the database. Enter 'n' to exit to return to the MAIN MENU.\n> ")

            while val not in ('y', 'n'):
                val = input ("Please enter a valid input:\n> ")

            match val:
                case 'y':
                    print ("Hooray!\n")

                    #.find() returns the size of the array
                    filledDocument = collection_name.find()
                    print("The not-so-clean way of displaying information from a document: \n")
                    for everyWholeEntry in filledDocument:    # For loop iterates 
                        print(everyWholeEntry)

                    dataFromDocument = collection_name.find()
                    print("\nThe kinda-clean way of displaying information from a document: \n")
                    for eachEntry in dataFromDocument:
                        print("Winner Name:", eachEntry['name'],"\nFilm they starred in:", eachEntry['film'],"\nDid they Win a Academy Award?:", eachEntry['winner'], "\n")

                case 'n':
                    print ("Boooo!")

                # This is in case something horrific happens
                case _:
                    print ("I'm a Spout! How did we get here?!?") 

        # The below will add one new, hardcoded entry, and check for a duplicate before doing so
        case '3':
            val = input ("Enter 'y' if you would like to UPDATE changes to the Academy. Enter 'n' to return to the MAIN MENU.\nNOTE: Will error if collection being written to is empty. If an entry already exists, a new one will not be made!\n> ")

            # Check input
            while val not in ('y', 'n'):
                val = input ("Please enter a valid input:\n> ")

            match val:
                case 'y':
                    print ("Hooray!")

                    #Add this entry
                    item_3 = {
                    "year_film" : 2025,
                    "year_ceremony" : 2025,
                    "ceremony" : 10,
                    "category" : "TEST",
                    "name" : "Caleb Trathen",
                    "film" : "Test for MongoDB Part 3: Ainsley Strikes Back",
                    "winner" : "False"
                    }

                    # Check for duplicate before doing so
                    try:
                        if collection_name.find_one(item_3):
                            print ("A duplicate entry was already found. Therefore no new entry was added.\n")
                        else:
                            collection_name.insert_one(item_3)
                            print ("New entry added.\n")
                    except:
                        print ("ERROR: Couldn't find or insert.\n")

                case 'n':
                    print ("Boooo!")
                
                # This is in case something horrific happens
                case _:
                    print ("I'm a teapot! How did we get here?!?")

        # The below will search by year for and display, all documents under a year category in the test branch
        case '4':
            val = input ("Enter the year to search to display all Academy Awards from that time period.\n> ")

            # Check input
            while (1927 > int(val) > 2025):
                val = input ("Please enter a valid year to search for entries from:\n> ")

            # Check for duplicate before doing so
            try:
                if collection_name.find_one({"year_film": int(val)}):
                    for eachEntry in collection_name.find({"year_film": int(val)}):
                        print("Winner Name:", eachEntry['name'],"\nFilm they starred in:", eachEntry['film'],"\nDid they Win a Academy Award?:", eachEntry['winner'], "\n")
                else:
                    print ("Match not found.\n")
            except:
                print ("ERROR: Couldn't search.\n")

        # The below will search by year and name for deleting a document
        case '5':
            val1 = input ("Enter the year to search.\n> ")

            # Check input
            while (1927 > int(val1) > 2025):
                val = input ("Please enter a valid year to search for entries from:\n> ")

            val2 = input ("Enter the actor's first and last name to search. NOTE: Name is Case Sensitve and must match entry exactly.\n> ")

            # Check for duplicate before doing so
            try:
                if collection_name.find_one({"year_film": int(val1), "name": val2}):
                    print ("Would you like to delete the following document?\n")
                    
                    #Display selected Docs
                    for eachEntry in collection_name.find({"year_film": int(val1), "name": val2}):
                        print("Winner Name:", eachEntry['name'],"\nFilm they starred in:", eachEntry['film'],"\nDid they Win a Academy Award?:", eachEntry['winner'], "\n")
                    
                    val = input ("Enter 'y' if you would like to delete the above document. Enter 'n' to return to Main Menu.\n> ")
                    # Check input
                    while val not in ('y', 'n'):
                        val = input ("Please enter a valid input:\n> ")

                    match val:
                        case 'y':
                            collection_name.delete_one({"year_film": int(val1), "name": val2})
                            print ("\nSelected document deleted.\n")
                        case 'n':
                            print ("\nDeletion canceled\n")
                        case _:
                            print ("\nERROR: Unexpected Input\n")
                else:
                    print ("No Documents found matching search term.\n")
            except:
                print ("ERROR: Couldn't search.\n")

        #Indexes, make them once, MongoDB will keep them up-to-date when new Documents are added. Index only needs to account for year.
        case '8':
            val = input ("Enter 'y' if you would like index the test collection using the year_film trait to speed up searching using thast trait. Please note that an Index only needs to be created once for a database, as MongoDB manages it from there. \nEnter 'n' to return to the MAIN MENU.\n> ")

            # Check input
            while val not in ('y', 'n'):
                val = input ("Please enter a valid input:\n> ")

            match val:
                case 'y':
                    print ("Hooray!")
                    collection_name.create_index([("year_film")])
                case 'n':
                    print ("Boooo!")
                # This is in case something horrific happens
                case _:
                    print ("I'm a teapot! How did we get here?!?")
        # This will end the loop, thereby ending the program
        case '9':
            break

        # This is in case something horrific happens
        case _:
            print ("Welcome to Hell, you go here before you die")
            break

# End program
client.close()      