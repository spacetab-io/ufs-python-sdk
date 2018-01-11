import requests
from xml.etree import ElementTree
from requests.auth import HTTPBasicAuth
from .exceptions import UfsAPIError, UfsTrainListError


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
        response_data = ElementTree.fromstring(response.text)
        if method == 'GetTicketBlank':
            if response_data.tag == 'html' or response.headers['Content-Type'] == 'application/pdf':
                return response

        if 'AdditionalInfo' in [item.tag for item in response_data]:
            raise UfsTrainListError(method, response_data)
        if 'Error' in [item.tag for item in response_data]:
            raise UfsAPIError(method, response_data)

        self.last_response_data = response_data

        return response_data

    def __send_api_request(self, method, params, get):
        if get:
            url = '{}/{}?terminal={}{}'.format(Session.API_URL, method, self.terminal, params)
            self.last_request_data = params
            response = self.requests_session.get(url, timeout=120)
            return response
        else:
            # post запрос, добавлю далее по необходимости
            pass
