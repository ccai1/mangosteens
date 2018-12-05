import base64
import requests
import json
from urllib import request, parse

'''
USE TOKEN AND HEADER
'''
client_id = "0ebc7e151f5840bf978bc22e81c87b45"
client_secret = "4b3388465d82493381bf58be352dfb1c"
authorize_url = "https://accounts.spotify.com/authorize"
access_token_url = "https://accounts.spotify.com/api/token"
base_url = "https://accounts.spotify.com/"
redirect_uri = "http://127.0.0.1:5000/callback/"

params = {'response_type': 'code',
          'redirect_uri': redirect_uri,
          "client_id": "0ebc7e151f5840bf978bc22e81c87b45"}

TOKEN = "AQA0k07MIMgwc33OlIzdv7SzPDMwmgb5QRgcm_2bdG5A-Oi87B_YRbzxFcAS0oEB6AuVEPd_MC0m2x-WZD1p-2pILkbICUXaTqbX-Tus0jALngSEKdNXpuZlhgjFYvN8xaEQqeLe2qWSKaYpl_dkpxtVMu3LIu5HbrYORYt8jsGYHmOOeaTXJQ4G8SKzwGT1Om0zMZViLQ"

def authorize(auth_token):
    code_payload = {
        'grant_type': 'client_credentials',
        "code": str(auth_token),
        'redirect_uri': redirect_uri
    }
    base64encoded = base64.b64encode(("{}:{}".format(client_id, client_secret)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post(access_token_url, data=code_payload,headers=headers)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

print(authorize(TOKEN))

HEADER = {'Authorization': 'Bearer BQDydasl9YP2sP7RV0sD42ZBuOyYwUtmUjEXX32xwQ1G-ti8882BiTP7WhQ_m44_kYsBrVgMJq30hQZAvIU'}

def search_tracks(query):
    URL = "https://api.spotify.com/v1/search?q={}&type={}"
    URL.format(query, "track")
    URL = request.Request(URL, headers = HEADER)
    print(URL)
    response = request.urlopen(URL)
    data = json.loads(response)
    return data

print(search_tracks("edm"))
#CODE = "AQBG3As_4b-5wKX17hKgoy20pzBQWL9KDs6jAa-vhG70Zrf0UeYV933Y9TsrMSNdJcYUciqTIbbnKr9eb9hBMCT0_L58W436yCL4-llu993OViHgnfIheqjxBaQTEfB5nQictsNhIN6hZ-Z8A00pgUdwSAB33UYHhMoR6IHGKd8Sbg4HqvVMfmlY9aGQcc2xUhGaZm5wBQ"
'''
session = spotify.get_auth_session(data={'code': 'AQBG3As_4b-5wKX17hKgoy20pzBQWL9KDs6jAa-vhG70Zrf0UeYV933Y9TsrMSNdJcYUciqTIbbnKr9eb9hBMCT0_L58W436yCL4-llu993OViHgnfIheqjxBaQTEfB5nQictsNhIN6hZ-Z8A00pgUdwSAB33UYHhMoR6IHGKd8Sbg4HqvVMfmlY9aGQcc2xUhGaZm5wBQ','redirect_uri': redirect_uri})

r = session.get('foo', params={'format': 'json'})
print (r.json())
'''
'''#https://github.com/mari-linhares/spotify-flask/blob/master/spotify_requests/spotify.py

import json
import base64
from urllib import request, parse

spotify_api_base_url = 'https://api.spotify.com'
api_version = "v1"
spotify_api_url = "{}/{}".format(spotify_api_base_url, api_version)

spotify_auth_base_url = "https://accounts.spotify.com/{}"
spotify_auth_url = spotify_auth_base_url.format('authorize')
spotify_token_url = spotify_auth_base_url.format('api/token')

client_id = "77cf833ba97d4dbfbbd887ba64c6c73c"
client_secret = "3f9ac93496244f04a95b6a4a216dc951"

redirect_uri = "http://127.0.0.1:5000/callback/"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "client_id": client_id
}


url_args = "&".join(["{}={}".format(key, parse.quote(val))
                for key, val in list(auth_query_parameters.items())])


auth_url = "{}/?{}".format(spotify_auth_url, url_args)


def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": redirect_uri
    }
    
    base64encoded = base64.b64encode(("{}:{}".format(client_id, client_secret)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(spotify_token_url, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header


def searchTracks(song, artist):
    URL= "https://api.spotify.com/v1/search?q=name:' + song + '%20artist:' + artist + '&type=track&limit=10"
    return URL
'''