#https://github.com/mari-linhares/spotify-flask/blob/master/spotify_requests/spotify.py

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


url_args = "&".join(["{}={}".format(key, urllibparse.quote(val))
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


