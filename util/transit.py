import json
from urllib import request, parse

def get_transit_info(location, destination, time_leaving): # hide key, vars for start/end address, key
    URL_STUB = "https://transit.api.here.com/v3/route.json?dep={},{}&arr={},{}&time={}&app_id={}&app_code={}"

    dep = get_geo(location)
    arr = get_geo(destination)

    dep_lat = dep["lat"]
    dep_long = dep["lng"]
    arr_lat = arr["lat"]
    arr_long = arr["lng"]

    # must be in format yyyy-mm-ddThh:mm:ss
    # must be at or after local time
    time = time_leaving
    app_id = "3yvzQG60zJIScGOHeEVK"
    app_code = "51NmvNiDfNtVqKmYgKBaMg"

    URL = URL_STUB.format(dep_lat, dep_long, arr_lat, arr_lat, time, app_id, app_code)
    print(URL)

    response = request.urlopen(URL)
    response = response.read()
    data = json.loads(response)
    return data

def get_geo(place):
    URL_STUB = "http://www.mapquestapi.com/geocoding/v1/address?key={}&location={}"

    key = "HetYdvBFjsiAKOqjuLAUOmCWrHaRvqDS"
    location = place

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


get_geo("345 Chambers St, New York, NY 10282")
