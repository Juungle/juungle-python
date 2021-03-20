import requests
import json

from juungle.common import LOGIN_USERNAME
from juungle.common import LOGIN_PASSWORD

URL_API = "https://www.juungle.net/api/v1"


class Auth():
    def __init__(self):
        self.token = self._get_token()

    def _get_token(self):
        data = {
            "email": LOGIN_USERNAME,
            "password": LOGIN_PASSWORD
        }
        api_url = "/user/login"

        response = self.call_post(api_url, data)
        if response.status_code == 200:
            return response.json()['jwtToken']
        else:
            raise BaseException('Login failed!')

    def call_post(self, url, data,
                  headers={'Content-Type': 'application/json'}):
        url = "{}/{}".format(URL_API, url)

        return requests.post(url, json=data, headers=headers)

    def call_get_json(self, url, data,
                      headers={'Content-Type': 'application/json'}):
        url = "{}/{}".format(URL_API, url)
        return requests.get(url, json=data, headers=headers)

    def call_get_query(self, url, data):
        url = "{}/{}".format(URL_API, url)
        return requests.get(url, params=data)
