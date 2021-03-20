"""Auth module."""
import configparser
import json
import os

import requests

URL_API = "https://www.juungle.net/api/v1"


class NoLoginProvided(Exception):
    pass


class NoPasswordProvided(Exception):
    pass


class LoginFailed(Exception):
    pass


class CommandFailed(Exception):
    pass


class FailedRequest(Exception):
    pass


class TooManyRequests(Exception):
    pass


class Auth():
    """Auth Class."""

    def __init__(self, login_user=None, login_pass=None):
        """init."""

        self.login_user = login_user
        self.login_pass = login_pass

        if not self.login_user or not self.login_pass:
            if os.path.exists('user-config.ini'):
                config = configparser.ConfigParser()
                config.read('user-config.ini')
                self.login_user = config['DEFAULT']['LOGIN_USERNAME']
                self.login_pass = config['DEFAULT']['LOGIN_PASSWORD']

        if not self.login_user:
            raise NoLoginProvided

        if not self.login_pass:
            raise NoPasswordProvided

    def _get_token(self):
        data = {
            "email": self.login_user,
            "password": self.login_pass
        }

        url = "{}/{}".format(URL_API, 'user/login')
        response = requests.post(url, json=data,
                                 headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print(response.json())
            if not response.json()['success']:
                raise CommandFailed('Login failed: {}'.format(
                    response.content))
            return response.json()['jwtToken']
        else:
            if response.status_code == 429:
                raise TooManyRequests

            raise LoginFailed("Login Failed")

    def _check_response(self, response):
        if response.status_code != 200:
            if response.status_code == 429:
                raise TooManyRequests
            raise FailedRequest('Request failed: {}'.format(response.content))

        if not response.json()['success']:
            raise CommandFailed('Login failed: {}'.format(response.content))

    def call_post(self, url, data, with_token=False,
                  headers={'Content-Type': 'application/json'}):
        """Methods post."""

        if with_token:
            headers['X-Access-Token'] = self._get_token()

        url = "{}/{}".format(URL_API, url)

        response = requests.post(url, json=data, headers=headers)
        self._check_response(response)

        return response

    def call_get_json(self, url, data, with_token=False,
                      headers={'Content-Type': 'application/json'}):

        if with_token:
            headers['X-Access-Token'] = self._get_token()

        url = "{}/{}".format(URL_API, url)
        return requests.get(url, json=data, headers=headers)

    def call_get_query(self, url, data):
        url = "{}/{}".format(URL_API, url)
        response = requests.get(url, params=data)
        self._check_response(response)
        return response
