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
    URL_STUB = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&page={}&api_key=" + key + "&format=json"

    page = 1
    URL = URL_STUB.format(page)

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    track_list = []

    counter = 0
    while(len(track_list) != num):
        track_data = data["tracks"]["track"][counter]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]

        if check_song(artist, track_name):
            track_list.append([artist, track_name])

        counter += 1

        if counter >= 50:
            counter = 0
            page += 1

    return track_list

'''
	Checks to see if song can be retrieved and has a duration of more than 0
	Returns True if it's a success otherwise, False
'''
def check_song(artist, name):

	try:
		info = get_track_info(artist, name)
	except:
		print("cannot access api")
		return False

	try:
		if get_track_duration(info) != 0:
			return True
	except:
		print("something wrong in the data retreived")
		return False


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
             print("Fixed") # Does not add the defective track
    return tracks


#print(check_song("lauv", "reforget"))

# print(get_top_tracks(20))

'''
Get top tracks by tags
Returns a list of artist + track name (same as get_top_tracks(num))
'''

def get_tracks(tag, num):
    URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + str(tag) + "&page={}&api_key=" + str(key) + "&format=json"
    #print (URL)

    page = 0

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)

    track_list = []

    counter = 0
    while(len(track_list) != num):
        track_data = data["tracks"]["track"][counter]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]

        if check_song(artist, track_name):
            track_list.append([artist, track_name])

        counter += 1

        if counter >= 50:
            counter = 0
            page += 1

    return track_list

'''
	Get a single track of a tag starting from that tag, counter, and page number
	Returns a list of [new counter, new page number, [artist, song name]]
'''

def get_tracks_custom(tag, counter, page):
    URL = "http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=" + str(tag) + "&page={}&api_key=" + str(key) + "&format=json"
    print (URL)

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)

    track_list = []

    while(True):
        track_data = data["tracks"]["track"][counter]
        artist = track_data["artist"]["name"]
        track_name = track_data["name"]

        if check_song(artist, track_name):
            counter += 1

            if counter >= 50:
                counter = 0
                page += 1

            return [counter, page, [artist, track_name]]

        counter += 1

        if counter >= 50:
            counter = 0
            page += 1

    return track_list

# print(get_tracks("happy", 5))

'''
Get top tracks from 1 to 3 tags regardless of order
    ex:
	'''


def get_tracks_tagged(tag0, tag1, tag2, num): # FUNCTIONAL, BUT MESSY (SLOW)
    tags = [tag0, tag1, tag2]
    count_list = [0, 0, 0]
    page_list = [0, 0, 0]

    track_list = []

    counter = 0

    if tags[0] == "None" and tags[1] == "None" and tags[2] == "None":
        return get_top_tracks(num)

    while (len(track_list) != num):
        if tags[counter % 3] != "None":
            data = get_tracks_custom(tags[counter % 3], count_list[counter % 3], page_list[counter % 3])

            count_list[counter % 3] = data[0]
            page_list[counter % 3] = data[1]
            track_list.append(data[2])
            #print(data)

        counter += 1

    return track_list

# print(get_tracks_tagged("edm", "None", "country", 5))
# print(get_tracks_tagged("edm", "None", "None", 3))
# print(get_tracks_tagged("edm", "pop", "country", 3))
# print(get_tracks_tagged("None", "None", "country", 3))
# print(get_tracks_tagged("None", "disco", "country", 3))
# print(get_tracks_tagged("happy", "life", "love", 5))

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
    #track_list = fix_track_list(track_list) # second fix for broken songs with 0 duration
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
    # track_list = []

	num = int(time / 223)

	playlist = get_tracks_tagged(tag0, tag1, tag2, num)
	time = get_total_time(playlist)
	print(time)
	return playlist

    # # NO tags given (top chart based)
    # if (tag0 == "None" and tag1 =="None" and tag2 == "None"):
    #     for num in range(1,50): # 50 searches per page max
    #         if time - get_total_time(get_top_tracks(num)) < 0:
    #             track_list = get_top_tracks(num) # triple checking for broken tracks
    #             break
    # else:
    #     # tags given
    #     for num in range(1,50):
    #         if time - get_total_time(get_tracks_tagged(tag0, tag1, tag2, num)) < 0:
    #                track_list = get_tracks_tagged(tag0, tag1, tag2,num)
    #                break
    # playlist = [] # adding URL to playlist
    # for track in track_list: # adds to wait time for generating playlists
    #     artist = track[0]
    #     track_name = track[1]
    #     track_url = get_track_url(get_track_info(artist, track_name))
    #     playlist.append([artist, track_name, track_url])

#print(gen_playlist(6000, "edm", "pop", "country"))
# print(gen_playlist(6000, "edm", "pop", "country")) # takes a couple seconds to gen the playlist
# print(get_tracks_tagged("edm", "None", "None", 6))
'''
print(get_total_time(get_top_tracks(3)))
print(gen_playlist(2000, "None"))
'''
