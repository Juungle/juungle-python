"""Auth module."""
import configparser
import os
import time

import requests

from juungle.rate_limiter import Limiter

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

        self._limiter = None

    def _get_token(self):
        data = {
            "email": self.login_user,
            "password": self.login_pass
        }

        url = "{}/{}".format(URL_API, 'user/login')
        if self._limiter:
            if self._limiter.rate_limit_remaining > 1:
                response = requests.post(url, json=data, headers={
                    'Content-Type': 'application/json'})
                self._limiter.update(response.headers)
            else:
                time.sleep(self._limiter.rate_limit_reset)
                response = requests.post(url, json=data, headers={
                    'Content-Type': 'application/json'})
                self._limiter.update(response.headers)
        else:
            response = requests.post(
                url, json=data, headers={'Content-Type': 'application/json'})
            self._limiter = Limiter(response.headers)

        if response.status_code == 200:
            print(response.json())
            if not response.json()['success']:
                raise CommandFailed('Login failed: {}'.format(
                    response.content))
            return response.json()['jwtToken']

        if response.status_code == 429:
            raise TooManyRequests

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

        if self._limiter:
            if self._limiter.rate_limit_remaining > 1:
                response = requests.post(url, json=data, headers=headers)
                self._limiter.update(response.headers)
            else:
                time.sleep(self._limiter.rate_limit_reset)
                response = requests.post(url, json=data, headers=headers)
                self._limiter.update(response.headers)
        else:
            response = requests.post(url, json=data, headers=headers)
            self._limiter = Limiter(response.headers)

        self._check_response(response)

        return response

    def call_get_json(self, url, data, with_token=False,
                      headers={'Content-Type': 'application/json'}):

        if with_token:
            headers['X-Access-Token'] = self._get_token()

        url = "{}/{}".format(URL_API, url)

        if self._limiter:
            if self._limiter.rate_limit_remaining > 1:
                response = requests.get(url, json=data, headers=headers)
                self._limiter.update(response.headers)
            else:
                print('Requests are too fast. Waiting a bit....')
                time.sleep(self._limiter.rate_limit_reset)
                print('Ok all good.. continue')
                response = requests.get(url, json=data, headers=headers)
                self._limiter.update(response.headers)
        else:
            response = requests.get(url, json=data, headers=headers)
            self._limiter = Limiter(response.headers)

        return response

    def call_get_query(self, url, data):
        url = "{}/{}".format(URL_API, url)
        response = requests.get(url, params=data)
        self._check_response(response)
        return response
