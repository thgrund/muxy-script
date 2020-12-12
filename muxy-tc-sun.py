import urllib.request, json 
from datetime import timedelta,datetime

import getopt
import sys
import requests
import random
import string

options, remainder = getopt.getopt(sys.argv[1:], 'ha:e:', [ 
                                                         'apiKey=',
                                                         'event='
                                                        ])
baseURL = "http://muxy.tidalcycles.org/"
eventURL = baseURL + "events/"
streamURL = baseURL + "streams/"
performanceDelta = timedelta(minutes=20)
streamKeys = {}

print("""
Create munix streams for an event based on sun.tidalcycles.org
Use --help to see the help.
""")

for opt, arg in options:
    if opt in ('-a', '--apiKey'):
        apiKey = arg
    elif opt in ('-e', '--event'):
        event = arg
    elif opt in ('-h', '--help'):
        print("""Available parameter:
    -a          Same as --apiKey      
    --apiKey    Use this apiKey from sun.tidalcycles.org
    -e          same as --event
    --event     Event id 
""")

def generateStreamKey():
    letters_and_digits = string.ascii_letters + string.digits
    streamKey = '-'.join(''.join((random.choice(letters_and_digits) for i in range(8))) for i in range(4))
    if(streamKey in streamKeys):
        generateStreamKey()
    else:
        return streamKey
    
def parseJsonFromSun(data):

    try:
        apiKey
    except NameError:
        print("ApiKey is not defined")
    else: 
        try:
            event
        except NameError:
            print("Event is not defined")
        else:
            performances = data["data"]
            starttime = datetime(2020, 12, 20, 14, 40)
            
            print("Start sending requests to muxy.tidalcycles.org")

            for performance in performances.values():
                sendToMuxy(performance, starttime)
                starttime = starttime + performanceDelta

            print("Finished")

def sendToMuxy(stream, time):
    headers = { "Content-Type": "application/json", 
            "Authorization": "Api-Key " + apiKey }

    payload = {
        "event": eventURL + event + "/", 
        "starts_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ends_at": (time+performanceDelta).strftime("%Y-%m-%dT%H:%M:%S"),
        "publisher_name": stream["name"], 
        "key": generateStreamKey()
    }

    r = requests.post(streamURL, json=payload, headers={'Content-Type':'application/json',
               'Authorization': 'Api-Key ' + apiKey}
    )   

    print ("Sending: " + json.dumps(payload))
    print (r)

with urllib.request.urlopen("https://sun.tidalcycles.org/api") as url:
    data = json.loads(url.read().decode())
    parseJsonFromSun(data)

