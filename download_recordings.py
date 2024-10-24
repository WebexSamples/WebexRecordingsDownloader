import requests
import json
import csv
import time

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def getDownloadLinks(headers):
    recordingDownloadLink = None
    with open ('recordings.csv', 'r') as csvfile:
        recs = csv.reader(csvfile)
        for row in recs:
            id = row[0]
            hostEmail = row[1].replace('@','%40').replace("+", "%2B")
            print("RecordingId: "+id+", HostEmail: "+hostEmail)
            url = 'https://webexapis.com/v1/recordings/'+id+'?hostEmail='+hostEmail
            #print(url)
            result = requests.get(url, headers=headers)
            downloadLink = json.loads(result.text)
            links = downloadLink['temporaryDirectDownloadLinks']
            recordingDownloadLink = links['recordingDownloadLink']
            print("Download Link: "+recordingDownloadLink)
            if recordingDownloadLink != None:
                try:
                    recording = requests.get(recordingDownloadLink)
                    if recording.status_code == 200:
                        fileName = recording.headers.get('Content-Disposition').split("''")[1]
                        print("Filename: "+str(fileName))
                        with open("Downloaded-Recordings/"+fileName, 'wb') as file:
                            file.write(recording.content)
                            print(fileName+" saved!")
                    elif recording.status_code == 429:
                        retry_after = recording.headers.get("retry-after") or recording.headers.get("Retry-After")
                        print("Rate limited. Waiting "+str(retry_after)+" seconds.")
                        time.sleep(int(retry_after))
                    else:
                        print("Unable to download, something went wrong!")
                        print("Status Code: "+str(recording.status_code))
                except Exception as e:
                    print(e)        
            else:
                print("something went wrong.")