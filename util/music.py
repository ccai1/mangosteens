import json
from urllib import request, parse

with open("data/keys.json") as f:
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
Returns the URL of the track (to play)
'''
def get_track_url(data):
    return data["track"]["url"]

#print(get_track_url(get_track_info("Alan Walker", "Faded")))
'''
Get a certain number of top tracks on chart
Returns a list of artist + track name:
    ex: get_top_tracks(2)
    [['Ariana Grande', 'Thank U, Next'], ['Queen', 'Bohemian Rhapsody - Remastered 2011']]
'''
def get_top_tracks(num):
    URL = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=" + key + "&format=json"
    #print (URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    track_list = []
    for x in range(num):
        track_data = data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        track_list.append([artist, track_name])
    track_list = fix_track_list(track_list)
    return track_list

'''
Fixing track list; removes tracks with 0 duration
Returns a new track list with only working tracks
'''
def fix_track_list(track_list):
    #print("Track List:")
    #print(track_list)
    tracks = []
    for track in track_list:
        artist = track[0]
        name = track[1]
        try:
            if get_track_duration(get_track_info(artist, name)) != 0:
                tracks.append(track)
        except:
            # print("Fixed") # Does not add the defective track
            '''
    for track in range(len(tracks)):
        artist = track[0]
        name = track[1]
        if get_track_duration(get_track_info(artist, name)) == 0:
            '''
    return tracks

'''

'''
def fix_song(song):
	if len(song) < 2:
		print("song does not meet length criteria of function")
		return False

	artist = track[0]
	name = track[1]

	try:
		info = get_track_info(artist, name)
	except:
		print("cannot access api")
		return False

	

'''
Get top tracks by tags
Returns a list of artist + track name (same as get_top_tracks(num))
'''
def get_tracks(tag, num):
    URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag + "&api_key=" + key + "&format=json"
    #print (URL)
    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    track_list = []
    for x in range(num):
        track_data = data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        #track_url = get_track_url(get_track_info(artist, track_name))
        track_list.append([artist, track_name])
    track_list = fix_track_list(track_list) # first fix
    return track_list

'''
Get top tracks from 1 to 3 tags regardless of order
    ex:
    print(get_tracks_tagged("edm", "None", "country", 5))
    print(get_tracks_tagged("edm", "None", "None", 3))
    print(get_tracks_tagged("edm", "pop", "country", 3))
    print(get_tracks_tagged("None", "None", "country", 3))
    print(get_tracks_tagged("None", "disco", "country", 3))
'''
def get_tracks_tagged(tag0, tag1, tag2, num): # FUNCTIONAL, BUT MESSY (SLOW)
    track_list = []
    if tag0 != "None" and tag1 != "None" and tag2 != "None":
        tag0_num = int(num / 3)
        tag1_num = int(num / 3)
        tag2_num = num - (tag0_num + tag1_num)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag0 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag0_data = json.loads(response)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag1 + "&api_key=" + key + "&format=json"
        response = request.urlopen(URL)
        response = response.read()
        tag1_data = json.loads(response)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag2 + "&api_key=" + key + "&format=json"
        response = request.urlopen(URL)
        response = response.read()
        tag2_data = json.loads(response)
        for x in range(tag0_num):
            track_data = tag0_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
        for x in range(tag1_num):
            track_data = tag1_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
        for x in range(tag2_num):
            track_list = fix_track_list(track_list) # first fix
            track_data = tag2_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 != "None" and tag1 == "None" and tag2 == "None":
        tag0_num = num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag0 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag0_data = json.loads(response)
        for x in range(tag0_num):
            track_data = tag0_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 == "None" and tag1 != "None" and tag2 == "None":
        tag1_num = num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag1 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag1_data = json.loads(response)
        for x in range(tag1_num):
            track_data = tag1_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 == "None" and tag1 == "None" and tag2 != "None":
        tag2_num = num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag2 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag2_data = json.loads(response)
        for x in range(tag2_num):
            track_data = tag2_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 != "None" and tag1 != "None" and tag2 == "None":
        tag0_num = int(num/2)
        tag1_num = num - tag0_num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag0 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag0_data = json.loads(response)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag1 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag1_data = json.loads(response)
        for x in range(tag0_num):
            track_data = tag0_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
        for x in range(tag1_num):
            track_data = tag1_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 != "None" and tag1 == "None" and tag2 != "None":
        tag0_num = int(num/2)
        tag2_num = num - tag0_num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag0 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag0_data = json.loads(response)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag2 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag2_data = json.loads(response)
        for x in range(tag0_num):
            track_data = tag0_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
        for x in range(tag2_num):
            track_data = tag2_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    elif tag0 == "None" and tag1 != "None" and tag2 != "None":
        tag2_num = int(num/2)
        tag1_num = num - tag2_num
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag2 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag2_data = json.loads(response)
        URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + tag2 + "&api_key=" + key + "&format=json"
        #print (URL)
        response = request.urlopen(URL)
        response = response.read()
        tag1_data = json.loads(response)
        for x in range(tag2_num):
            track_data = tag2_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
        for x in range(tag1_num):
            track_data = tag1_data["tracks"]["track"][x]
            artist = track_data["artist"]["name"]
            track_name = track_data["name"]
            #track_url = get_track_url(get_track_info(artist, track_name))
            track_list.append([artist, track_name])
    else:
        print("Use the top charts method, not this one!")
    track_list = fix_track_list(track_list) # first fix
    return track_list

    #elif:
    #    return track_list
'''
    for x in range(num):
        track_data = tag1_data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        #track_url = get_track_url(get_track_info(artist, track_name))
        track_list.append([artist, track_name])
    track_list = fix_track_list(track_list) # first fix
    for x in range(num):
        track_data = tag2_data["tracks"]["track"][x]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]
        #track_url = get_track_url(get_track_info(artist, track_name))
        track_list.append([artist, track_name])
'''
'''
TESTING CODE ABOVE

print(get_tracks_tagged("edm", "None", "country", 3))
print(get_tracks_tagged("edm", "None", "None", 3))
print(get_tracks_tagged("edm", "pop", "country", 3))
print(get_tracks_tagged("None", "None", "country", 3))
print(get_tracks_tagged("None", "disco", "country", 3))
#print(get_top_tracks(5))
#print(get_tracks("holidays", 3))
#print(get_track_duration(get_track_info("Alan Walker", "Faded")))
'''
'''
Returns the total duration of a track list
'''
def get_total_time(track_list):
    total_time = 0
    track_list = fix_track_list(track_list) # second fix for broken songs with 0 duration
    for track in track_list:
            artist = track[0]
            name = track[1]
            total_time += get_track_duration(get_track_info(artist, name))
    return total_time

#print("Time : " + str(get_total_time(get_tracks("edm", 10))))

'''
The playlist maker method according to time
Returns a track list as per the tags or top charts if tags are not giving that will add up to total time
'''
def gen_playlist (time, tag0, tag1, tag2):
    track_list = []
    # NO tags given (top chart based)
    if (tag0 == "None" and tag1 =="None" and tag2 == "None"):
        for num in range(1,50): # 50 searches per page max
            if time - get_total_time(get_top_tracks(num)) < 0:
                track_list = fix_track_list(get_top_tracks(num)) # triple checking for broken tracks
                break
    else:
        # tags given
        for num in range(1,50):
            if time - get_total_time(get_tracks_tagged(tag0, tag1, tag2, num)) < 0:
                   track_list = fix_track_list(get_tracks_tagged(tag0, tag1, tag2,num))
                   break
    playlist = [] # adding URL to playlist
    for track in track_list: # adds to wait time for generating playlists
        artist = track[0]
        track_name = track[1]
        track_url = get_track_url(get_track_info(artist, track_name))
        playlist.append([artist, track_name, track_url])
    return playlist

print(gen_playlist(1000, "edm", "pop", "country"))

'''
print(get_total_time(get_top_tracks(3)))
print(gen_playlist(1000, "edm")) # takes a couple seconds to gen the playlist
print(gen_playlist(2000, "None"))
'''
