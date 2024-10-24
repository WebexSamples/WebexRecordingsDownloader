import requests
import datetime
import json
import os
import time
import csv

def token_refresh():
    url = "https://webexapis.com/v1/access_token"
    refresh_headers = {"Accept" : "application/json","Content-Type":"application/json"}
    data = {
        "grant_type":"refresh_token",
        "client_id":os.getenv('client_id'),
        "client_secret":os.getenv('client_secret'),
        "refresh_token":os.getenv('refresh_token')
    }
    count = 0
    while count < 4:
        newToken = requests.post(url, json=data, headers=refresh_headers)
        count += 1
        if count == 3:
            break
    return newToken

def storeRecordings(items):
    for id in items:
        recordId = id['id']
        hostEmail = id['hostEmail']
        print(recordId, hostEmail)
        path = os.path.dirname(os.path.abspath(__file__))
        name = os.path.join(path, 'recordings.csv')
        with open (name, 'a', newline='') as writeRecordings:
            writer = csv.writer(writeRecordings, delimiter=',')
            writer.writerow((recordId, hostEmail))

def list(headers, site_url, weeks):
    to_time = datetime.datetime.now().replace(microsecond=0)
    from_time = to_time - datetime.timedelta(days=30)
    end_time = from_time - datetime.timedelta(weeks=int(weeks))
    #print(to_time)
    #print(from_time)
    more = True
    count = 0
    while more == True:
        try:
            url = "https://webexapis.com/v1/admin/recordings?siteUrl={0}&max=100&from={1}&to={2}".format(site_url, from_time, to_time)
            print("URL: "+url)
            #print(headers)
            response = requests.get(url, headers=headers)
            if response.status_code == 401:
                if os.getenv('client_id') == "" or os.getenv('client_secret') == "" or os.getenv('refresh_token') == "":
                    print("Unable to refresh token. \nAdd your integration detials, client_id, client_secret and refresh_token, to the .env file and restart the app in order for it to handle refreshing your access token automatically.")
                    break
                else:
                    print("Token expired, generating new one...")
                    newTokenCreate = token_refresh()
                    if newTokenCreate.status_code != 200:
                        print("Oh no... Something went wrong!\nEither the access token provided or stored is not valid or unable to refresh access token due to invalid parameter(s) in the .env file.")
                        print("Error response:")
                        print(newTokenCreate.text)
                        break
                    else:
                        res = json.loads(newTokenCreate.text)
                        print("New Token: " +str(res['access_token']))
                        newToken = res['access_token']
                        bearer = {"token":newToken}
                        headers = {
                            "Accept":"application/json",
                            "Content-Type":"application/json",
                            "Authorization":"Bearer "+str(bearer['token'])
                            }
                        with open('token.json', 'w') as updateToken:
                            json.dump(bearer, updateToken)
            elif response.status_code == 200:
                print("Status Code: "+str(response.status_code))
                print("Response: "+str(response.text))
                recordings = json.loads(response.text)
                items = recordings['items']
                if items != []:
                    storeRecordings(items)
                count += 1
                print("Page Count: {0}\n".format(str(count)))
                while response.headers.get("link") != None:
                    url = response.headers.get("link").strip()[1:].split(">")[0]
                    print("URL: "+url)
                    try:
                        response = requests.get(url, headers=headers)
                        if response.status_code == 200:
                            print("Status Code: "+str(response.status_code))
                            print("Response: "+str(response.text))
                            count += 1
                            print("Page Count: {0}".format(str(count)))
                            result = json.loads(response.text)
                            items = result['items']
                            storeRecordings(items)
                        else:
                            print("Didn't work!")
                    except Exception as e:
                        print(e)
                else:
                    to_time = from_time
                    from_time = to_time - datetime.timedelta(days=30)
                if end_time > from_time:
                    more = False
                    print("Pulled the past " + weeks + " weeks of recordings.")
                    return(False)
            elif response.status_code == 429:
                retry_after = response.headers.get("retry-after") or response.headers.get("Retry-After")
                print("Rate limited. Waiting "+str(retry_after)+" seconds.")
                time.sleep(int(retry_after))
            else:
                print("Something went wrong!")
                print(response.text)
                break
        except Exception as e:
            print(e)
    