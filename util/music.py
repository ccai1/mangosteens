import json
from urllib import request, parse

with open("../data/keys.json") as f:
	api_keys = json.load(f)

key = api_keys["tracks_key"]

def get_track_info(artist, track):
    URL_STUB = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo"
    URL = URL_STUB + "&api_key=" + key + "&artist=" +artist + "&track=" +track + "&format=json"
    #print(URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    #print(URL)
    return data

def get_track_duration(data):
    return data["track"]["duration"]

def get_top_tracks():
    URL = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=" + key + "&format=json"
    print (URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    return data

#print(get_top_tracks())