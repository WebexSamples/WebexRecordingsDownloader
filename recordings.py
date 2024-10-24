import json
from list_recordings import *
from download_recordings import *

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

tokenPath = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(tokenPath, 'token.json')
with open (filename, 'r') as openfile:
    token = json.load(openfile)
    bearer = token["token"]
    if bearer == "":
        print("No stored token. \nEnter your access token.\n")
        token = input("> ")
        while token == "":
            print("No token entered. Try again.\n")
            token = input("> ")
        bearer = {"token":token}
        with open('token.json', 'w') as updateToken:
            json.dump(bearer, updateToken)
    else:
        print('Current Token: '+str(bearer))

headers = {
    "Accept":"application/json",
    "Content-Type":"application/json",
    "Authorization":"Bearer "+str(bearer)
    }

if not os.path.exists("Downloaded-Recordings/"):
    os.makedirs("Downloaded-Recordings/")

print("This app can be used to collect all recordingIds and associated hostEmails and then download all recordings locally.")
print("First you'll choose option 1 to collect recording data and the app will terminate.")
print("After all recording data has been collected then run the app again and choose option 2 to download all recordings.\n")
print("Select an option:")
print("1 - List all recordings and save to .csv file.")
print("2 - Download recordings.\n")
run = True
while run == True:
    choice = input("> ")
    print("You selected "+choice)
    try:
        if choice == "1":
            site_url = input("Enter the Webex site URL you want to pull recordings from.\nFor example: sitename.webex.com.  \n\n> ")
            weeks = input("Enter the number of weeks you would like to pull recording data for. \n\n> ")
            print("Listing recordings and saving to file, please wait...\n")
            result = list(headers, site_url, weeks)
            print("Finished!")
            run = result
        elif choice == "2":
            print("Downloading recordings...\n")
            result = getDownloadLinks(headers)
            print("Finished!")
            run = result
        else:
            print("Invalid option.\nTry again.\n\n> ")
    except Exception as e:
        print(e)