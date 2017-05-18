import hmac
import json
from hashlib import sha1

import requests
from django.conf import settings
from requests import Response
from rest_framework import status

from PACouchsurfing.settings import get_secret


class RequestError(Exception):
    def __init__(self, response: Response):
        self.message = 'Error. Status code: {}. Error: {}'.format(response.status_code, response.json())


class CouchsurfingService:
    def __init__(self, email: str, password: str):
        self.session = requests.Session()
        self.session.headers = self._default_headers
        self._uid, self._access_token = self._login(email, password)
        self.session.headers['X-Access-Token'] = self._access_token

    @property
    def _private_key(self) -> str:
        return get_secret('COUCHSURFING_PRIVATE_KEY')

    @property
    def _default_headers(self) -> dict:
        return {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en;q=1',
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.1;'
                          ' Android SDK built for x86 Build/LSX66B) Couchsurfing'
                          '/android/20141121013910661/Couchsurfing/3.0.1/ee6a1da'
        }

    def get_friendlist(self, uid: str = None, per_page: int = 999999999) -> dict:
        """
        Ask for friendlist for specific user
        """
        if uid is None:
            uid = self._uid

        path = '/api/v3.1/users/{uid}/friendList/friends?perPage={per_page}&' \
               'page=1&includeMeta=false'.format(uid=uid, per_page=per_page)

        return self._make_get_request(path)

    def _login(self, email: str, password: str) -> (str, str):
        assert (email and password)
        login_payload = {'actionType': 'manual_login',
                         'credentials': {'email': email, 'authToken': password}}
        self._update_headers_with_signature(key=self._private_key,
                                            msg='/api/v3/sessions' + json.dumps(login_payload))

        url = '{base_url}/api/v3/sessions'.format(base_url=settings.COUCHSURFING_URL)
        response = self.session.post(url, data=json.dumps(login_payload))

        data = response.json()
        if not status.is_success(response.status_code):
            raise RequestError(response)

        try:
            access_token = data['sessionUser']['accessToken']
        except KeyError:
            msg = 'No access token found in response.\n{}'.format(data)
            raise KeyError(msg)

        try:
            uid = data['sessionUser']['id']
        except KeyError:
            msg = 'No user id found in response.\n{}'.format(data)
            raise KeyError(msg)

        return uid, access_token

    def _update_headers_with_signature(self, key: str, msg: str):
        signature = hmac.new(key.encode('utf-8'), msg.encode('utf-8'), sha1).hexdigest()
        self.session.headers['X-CS-Url-Signature'] = signature

    def _make_get_request(self, path: str, params: dict = None):
        assert (self._access_token and self._uid)

        url = settings.COUCHSURFING_URL + path
        self._update_headers_with_signature(key='{}.{}'.format(self._private_key, self._uid), msg=path)

        response = self.session.get(url, params=params)

        if not status.is_success(response.status_code):
            print(json.dumps(self.session.headers, indent=4))
            print(response.json())
            raise RequestError(response)

        return response.json()
