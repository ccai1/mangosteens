import json
from urllib import request, parse

def getDirectionsInfo(): # hide key, vars for start/end address, key
    URL_STUB = "http://www.mapquestapi.com/directions/v2/route?"
    KEY = "HetYdvBFjsiAKOqjuLAUOmCWrHaRvqDS"
    starting_address = "Clarendon Blvd,Arlington,VA"
    end_address = "2400+S+Glebe+Rd,+Arlington,+VA"
    URL = URL_STUB + "key=" + KEY + "&from=" + fix_address(starting_address) + "&to=" + fix_address(end_address)
    response = request.urlopen(URL) 
    response = response.read()
    data = json.loads(response)
    return data

def fix_address(address):
    fixed = parse.quote(address)
    return fixed

print(getDirectionsInfo())

