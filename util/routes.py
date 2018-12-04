import json
from urllib import request, parse

'''
Getting json data from mapquest api (directions api)
route_type can be either fastest, shortest, pedestrian, or bicycle
'''
def getDirectionsInfo(start, end, route_type):
    try:
        KEY = "HetYdvBFjsiAKOqjuLAUOmCWrHaRvqDS"
        URL_STUB = "http://www.mapquestapi.com/directions/v2/route?"
        starting_address = fix_address(start)
        end_address = fix_address(end)
        URL = URL_STUB + "key=" + KEY + "&from=" + starting_address + "&to=" + end_address + "&routeType=" + route_type
        print(URL)
        response = request.urlopen(URL)
        response = response.read()
        data = json.loads(response)
        return data
    except:
        return False

'''
Fix the address to a working url
'''
def fix_address(address):
    #fixed = parse.quote(address)
    fixed = address.replace("&", " ")
    fixed = address.replace(" ", "%20")
    return fixed

'''
Returns realtime commute time
'''
def get_time(data):
    return data['route']['formattedTime']

'''
Returns distance of the route
'''
def get_distance(data):
    return data['route']['distance']

'''
Returns a list of map urls
'''
def get_maps(data):
    amt = len(data['route']['legs'][0]['maneuvers'])
    #print(amt)
    maps = []
    #print (data['route']['legs'][0]['maneuvers'][1]['mapUrl'])
    #print (data['route']['legs'][0]['maneuvers'][6]['mapUrl'])
    for x in range(0,amt-1):
        map = data['route']['legs'][0]['maneuvers'][x]['mapUrl']
        #print(map)
        maps.append(map)
    return maps

'''
Returns a list of directions
'''
def get_directions(data):
    amt = len(data['route']['legs'][0]['maneuvers'])
    directions = []
    for x in range(amt):
        direction = data['route']['legs'][0]['maneuvers'][x]['narrative']
        directions.append(direction)
    return directions

print(get_directions(getDirectionsInfo("345 Chambers St, New York, NY 10282","270 Greenwich St, New York","pedestrian")))
