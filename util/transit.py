import json
from urllib import request, parse
from datetime import datetime

"""
    Gets the data of the directions to the desired location
    Returns a list of possible routes
    Parameters: location -> starting address
                destination -> ending address

    To-do:
        Check to make sure that addresses are appropriate and return geocodes
"""
def get_transit_info(location, destination): # hide key, vars for start/end address, key
    URL_STUB = "https://transit.api.here.com/v3/route.json?dep={},{}&arr={},{}&time={}&app_id={}&app_code={}"

    dep = get_geo(location)
    arr = get_geo(destination)

    dep_lat = dep["lat"]
    dep_long = dep["lng"]
    arr_lat = arr["lat"]
    arr_long = arr["lng"]

    time = curr_time()
    app_id = "3yvzQG60zJIScGOHeEVK"
    app_code = "51NmvNiDfNtVqKmYgKBaMg"

    URL = URL_STUB.format(dep_lat, dep_long, arr_lat, arr_long, time, app_id, app_code)
    print(URL)

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)

    routes = data["Res"]["Connections"]["Connection"]

    #print(routes)
    return routes

########################################
#####   START OF GETS FROM ROUTE   #####
########################################


"""
    Returns the total time for a single route
    Parameter: data -> one possible route
    Ex: total_time( get_transit_info( something1, something2 )[ 0 ] )

    To-do:
        try except
"""
def get_total_time(data):
    return data["duration"][2:]

"""
    Returns the number of transfers for a single route
    Parameter: data -> one possible route
"""
def get_num_transfers(data):
    return data["transfers"]

"""
    Get the directions of a single route
    Returns a list where each element contains information via a dictionary on a single step in the route
"""
def get_directions(data):
    directions = data["Sections"]["Sec"]

    mode = {0 : "high speed train",
            1 : "intercity train",
            2 : "inter regional train",
            3 : "regional train",
            4 :	"city train",
            5 :	"bus",
            6 :	"ferry",
            7 :	"train",
            8 :	"light rail",
            9 :	"private bus",
            10 : "inclined",
            11 : "aerial",
            12 : "bus rapid",
            13 : "monorail",
            14 : "flight",
            }

    ret = []

    for step in directions:
        dicts = {}
        dicts["time"] = step["Journey"]["duration"][2:] # time to complete single step

        if step["mode"] == 20:
            dir = "Walk to "

            if "Stn" in step["Arr"].keys():
                dir += step["Arr"]["Stn"]["name"] + " station."
            else:
                dir += "destination."
        else:

            dir = "Take the {} {} headed towards {} for {} stops. Get off at {}."

            transit_name = step["Dep"]["Transport"]["name"]
            transit_type = mode[step["mode"]]
            towards = step["Dep"]["Transport"]["dir"]

            num_stops = len( step["Journey"]["Stop"] )
            dest = step["Arr"]["Stn"]["name"] + " station"

            dir = dir.format(transit_name, transit_type, towards, num_stops, dest)


        dicts["dir"] = dir
        ret.append(dicts)

    return ret



######################################
#####   END OF GETS FROM ROUTE   #####
######################################


"""
    Acquire the geocode of any address
    Parameter: place -> legitamate address

    To-do:
        Check to make sure an incorrect address isn't entered
        if it is then soemthing should be returned.
"""
def get_geo(place):
    URL_STUB = "http://www.mapquestapi.com/geocoding/v1/address?key={}&location={}"

    key = "HetYdvBFjsiAKOqjuLAUOmCWrHaRvqDS"
    location = fix_url(place)

    URL = URL_STUB.format(key, location)
    print(URL)
    print()

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)

    #print(data)

    geo_code = data["results"][0]["locations"][0]["latLng"]
    print(geo_code)

    return geo_code

"""
    Fixes the address to make it appropriate for the api to take in
    Parameter; place -> address
"""
def fix_url(place):
    place = place.replace(" ", "%20")
    place = place.replace("&", "")
    return place

"""
    Returns a time appropriate to use for acquiring directions
"""
def curr_time():
    # must be in format yyyy-mm-ddThh:mm:ss
    # must be at or after local time
    "2018-12-02 16:18:58.718602"
    t = str(datetime.now())
    t = t.split(" ")
    time = t[0]
    time += "T{}%3A{}%3A00"

    ti = t[1].split(":")

    if ti[1] == "55":
        hour = int(ti[0]) + 1
        if hour < 10:
            hour = "0" + str(hour)
        else:
            hour = str(hour)
    else:
        hour = int(ti[0])

    minute = (int(ti[1]) + 5) % 60

    time = time.format(hour, minute)

    print(time)
    return time



now = "345 Chambers St New York NY 10282"
to = "116th St & Broadway, New York, NY 10027"

get_geo(now)
get_geo(to)

rou = get_transit_info(now, to)

print(get_total_time(rou[0]))
print("\n Getting the directions to the first route: ")
print(get_directions(rou[0]))
