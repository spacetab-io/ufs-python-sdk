import requests
import logging
from xml.etree import ElementTree
from requests.auth import HTTPBasicAuth
from .exceptions import UfsAPIError, UfsTrainListError


class Session(object):
    API_URL = 'https://www.ufs-online.ru/webservices/Railway/Rest/Railway.svc'

    def __init__(self, username, password, terminal, logger: logging.Logger=None):
        self.username = username
        self.password = password
        self.terminal = terminal

        self.requests_session = requests.Session()
        self.requests_session.headers['Content-Encoding'] = 'gzip'
        self.requests_session.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.requests_session.auth = HTTPBasicAuth(self.username, self.password)

        self.last_response_data = None
        self.last_request_data = None

        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.Logger('empty', logging.NOTSET)

    def make_api_request(self, method, params=None, xml=None):
        response = self.__send_api_request(method, params, xml)
        if method == 'GetTicketBlank':
            if response.headers['Content-Type'] == 'application/pdf' or response.headers['Content-Type'] == 'text/html':
                return response
        response_data = ElementTree.fromstring(response.text)

        #if 'AdditionalInfo' in [item.tag for item in response_data]:
        #    raise UfsTrainListError(method, response_data)
        if 'Error' in [item.tag for item in response_data]:
            raise UfsAPIError(method, response_data)

        self.last_response_data = response_data

        return response_data

    def __send_api_request(self, method, params=None, xml=None):
        if xml is None:
            url = '{}/{}?terminal={}{}'.format(Session.API_URL, method, self.terminal, params)
            self.logger.debug('Request: %s',  url)
            self.last_request_data = params
            response = self.requests_session.get(url, timeout=120)
            self.logger.debug('Response for: %s\n%s',  url, response)
            return response
        else:
            url = '{}/{}?terminal={}'.format(Session.API_URL, method, self.terminal)
            self.last_request_data = xml
            self.logger.debug('Request:\n   Url: %s\n   XML: %s', url, ElementTree.tostring(xml))
            response = self.requests_session.post(url, data=ElementTree.tostring(xml, encoding='utf8'), 
                                                    headers={'Content-Type': '', 'Content-Encoding': 'gzip'})
            self.logger.debug('Response:\n   Url: %s\n   XML: %s\n   Response: %s', url, xml, response.text)
            return response
