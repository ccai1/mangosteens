import json
from urllib import request, parse

with open("../data/keys.json") as f:
	api_keys = json.load(f)

key = api_keys["tracks_key"]

'''
Returns the data for other methods
Params include artist and track name
    ex: (Alan Walker, Faded)
'''
def get_track_info(artist, track):
    URL_STUB = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo"
    URL = URL_STUB + "&api_key=" + key + "&artist=" +artist + "&track=" +track + "&format=json"
    #print(URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    #print(URL)
    return data

'''
Returns duration of the track
'''
def get_track_duration(data):
    return int(data["track"]["duration"]) / 1000

'''
Get a certain number of top tracks on chart
Returns a list of artist + track name:
    ex: get_top_tracks(2)
    [['Ariana Grande', 'Thank U, Next'], ['Queen', 'Bohemian Rhapsody - Remastered 2011']]
'''
def get_top_tracks(num):
    URL = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=" + key + "&format=json"
    print (URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    track_list = []
    for x in range(num):
        track_data = data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        track_list.append([artist, track_name])
    return track_list

'''
Fixing track list; removes tracks with 0 duration
Returns a new track list with only working tracks
'''
def fix_track_list(track_list):
    print("Track List:")
    print(track_list)
    tracks = []
    for track in track_list:
        artist = track[0]
        name = track[1]
        try:
            if get_track_duration(get_track_info(artist, name)) > 0:
                tracks.append(track)
        except:
            print("Fixed")
    print(tracks)
    return tracks


'''
Get top tracks by tags
Returns a list of artist + track name (same as get_top_tracks(num))
'''
def get_tracks(tag, num):
    URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag + "&api_key=" + key + "&format=json"
    print (URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    track_list = []
    for x in range(num):
        track_data = data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        track_list.append([artist, track_name])
    return track_list



print(get_top_tracks(5))
print(get_tracks("holidays", 3))
print(get_track_duration(get_track_info("Alan Walker", "Faded")))

'''
Returns the total duration of a track list
'''
def get_total_time(track_list):
    total_time = 0
    track_list = fix_track_list(track_list)
    for track in track_list:
            artist = track[0]
            name = track[1]
            total_time += get_track_duration(get_track_info(artist, name))
    return total_time

print("Time : " + str(get_total_time(get_tracks("edm", 10))))

'''
The playlist maker method
Returns a track list as per the tags or top charts if tags are not giving that will add up to total time
'''
def gen_playlist (time, tag, isTagged):
    track_list = []
    return track_list
