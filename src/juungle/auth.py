"""Auth module."""
import configparser
import json

import requests

URL_API = "https://www.juungle.net/api/v1"


class Auth():
    """Auth Class."""

    def __init__(self):
        """init."""
        config = configparser.ConfigParser()
        config.read('user-config.ini')
        self.login_user = config['DEFAULT']['LOGIN_USERNAME']
        self.login_pass = config['DEFAULT']['LOGIN_PASSWORD']

    def _get_token(self):
        data = {
            "email": self.login_user,
            "password": self.login_pass
        }

        url = "{}/{}".format(URL_API, 'user/login')
        response = requests.post(url, json=data,
                                 headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            return response.json()['jwtToken']
        else:
            raise BaseException('Login failed: {}'.format(response.content))

    def call_post(self, url, data, with_token=False,
                  headers={'Content-Type': 'application/json'}):
        """Methods post."""

        if with_token:
            headers['X-Access-Token'] = self._get_token()

        url = "{}/{}".format(URL_API, url)

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise BaseException('Request failed: {}'.format(response.content))

        if not response.json()['success']:
            raise BaseException('Request failed: {}'.format(response.content))

        return response

    def call_get_json(self, url, data, with_token=False,
                      headers={'Content-Type': 'application/json'}):

        if with_token:
            headers['X-Access-Token'] = self._get_token()

        url = "{}/{}".format(URL_API, url)
        return requests.get(url, json=data, headers=headers)

    def call_get_query(self, url, data):
        url = "{}/{}".format(URL_API, url)
        return requests.get(url, params=data)
