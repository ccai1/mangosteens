import json
from urllib import request, parse
'''
Getting json data from mapquest api (directions api)
'''
def getDirectionsInfo(key, start, end):
    URL_STUB = "http://www.mapquestapi.com/directions/v2/route?"
    KEY = key
    starting_address = start
    end_address = end
    URL = URL_STUB + "key=" + KEY + "&from=" + fix_address(starting_address) + "&to=" + fix_address(end_address)
    print(URL)
    response = request.urlopen(URL) 
    response = response.read()
    data = json.loads(response)
    return data

'''
Fix the address to a working url
'''
def fix_address(address):
    #fixed = parse.quote(address)
    fixed = address.replace(" ", "%20")
    return fixed

'''

'''
def getRoutes(data):
    return data['route']['legs'][0]['maneuvers']

'''
Returns realtime commute time
'''
def get_time(data):
    return data['route']['realtime']

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
    print(amt)
    maps = []
    #print (data['route']['legs'][0]['maneuvers'][1]['mapUrl'])
    #print (data['route']['legs'][0]['maneuvers'][6]['mapUrl'])
    for x in range(0,amt-1):
        map = data['route']['legs'][0]['maneuvers'][x]['mapUrl']
        #print(map)
        maps.append(map)
    return maps
    
print(get_maps(getDirectionsInfo("HetYdvBFjsiAKOqjuLAUOmCWrHaRvqDS","Clarendon Blvd,Arlington,VA","2400+S+Glebe+Rd,+Arlington,+VA")))


