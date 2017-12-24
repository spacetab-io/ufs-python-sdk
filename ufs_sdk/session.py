import json
import requests
from xml.etree import ElementTree
from requests.auth import HTTPBasicAuth
from .exceptions import UfsAPIError


class Session(object):
    API_URL = 'https://www.ufs-online.ru/webservices/Railway/Rest/Railway.svc'

    def __init__(self, username, password, terminal):
        self.username = username
        self.password = password
        self.terminal = terminal

        self.requests_session = requests.Session()
        self.requests_session.headers['Content-Encoding'] = 'gzip'
        self.requests_session.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.requests_session.auth = HTTPBasicAuth(self.username, self.password)

        self.last_response_data = None
        self.last_request_data = None

    def make_api_request(self, method, params, get):
        response = self.__send_api_request(method, params, get)
        response = ElementTree.fromstring(response.text)
        for item in response:
            if item.tag == 'Error':
                raise UfsAPIError(method, response, params)

        self.last_response_data = response

        return response

    def __send_api_request(self, method, params, get):
        if get:
            url = '{}/{}?terminal={}{}'.format(Session.API_URL, method, self.terminal, params)
            self.last_request_data = params
            response = self.requests_session.get(url, timeout=120)
            return response
        else:
            # post запрос, добавлю далее по необходимости
            pass
