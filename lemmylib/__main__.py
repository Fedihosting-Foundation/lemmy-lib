import logging
import os
from enum import Enum

import requests

if os.getenv("LOG_LEVEL") is None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=int(os.getenv("LOG_LEVEL")))


class LemmyApiMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


API_VERSION = "v3"


class LemmyLib:
    _jwt: str | None = None
    _url: str | None = None
    _logger: logging.Logger = None

    def __init__(self, url: str = None, jwt: str = None):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("LemmyLib init")
        if url is not None:
            if url.endswith("/"):
                url = url[:-1]
            self.set_url(url)
        if jwt is not None:
            self.set_jwt(jwt)

    def call_api(self, method: LemmyApiMethod, endpoint: str, params: dict = None, headers: dict = None,
                 data: dict = None):
        self._logger.debug("LemmyLib call_api")
        if headers is None:
            headers = self.get_headers()
        if params is None:
            params = {}
        if data is None:
            data = {}
        if self._url is None:
            raise Exception("LemmyLib: URL not set")

        url = f'{self._url}{self.get_base_path()}{endpoint}'

        self._logger.debug(f"LemmyLib call_api: {method} {url} {params} {headers} {data}")

        if method == LemmyApiMethod.GET:
            response = requests.get(url, params=params, headers=headers)
        elif method == LemmyApiMethod.POST:
            response = requests.post(url, params=params, headers=headers, json=data)
        elif method == LemmyApiMethod.PUT:
            response = requests.put(url, params=params, headers=headers, json=data)
        elif method == LemmyApiMethod.DELETE:
            response = requests.delete(url, params=params, headers=headers)
        else:
            raise Exception("LemmyLib: Unknown method")

        self._logger.debug(f"LemmyLib call_api: {response.status_code} {response.text}")

        if response.status_code == 200:
            return response
        else:
            raise Exception(
                f"LemmyLib: API call failed with status code {response.status_code} and message {response.text}")

    def get_base_path(self):
        return f'/api/{API_VERSION}/'

    def set_jwt(self, jwt: str):
        self._jwt = jwt
        self._logger.debug("LemmyLib set_jwt")

    def set_url(self, url: str):
        self._url = url
        self._logger.debug("LemmyLib set_url")

    def get_headers(self):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'lw-lemmy-lib',
        }
        if self._jwt:
            header['Authorization'] = f'Bearer {self._jwt}'

        return header

    def get_url(self):
        return self._url

    def get_jwt(self):
        return self._jwt

    def get_logger(self):
        return self._logger

    def login(self, username: str, password: str, totp: str | None = None, only_jwt: bool = False):
        self._logger.debug("LemmyLib login")
        response = self.call_api(LemmyApiMethod.POST, 'login',
                                 data={'username_or_email': username, 'password': password, 'totp_2fa_token': totp})

        if not only_jwt:
            self.set_jwt(response.json()["jwt"])

        return response

    def list_registration_applications(self, page: int = 1, unread_only: bool = False):
        self._logger.debug("LemmyLib list_registration_applications")

        return self.call_api(LemmyApiMethod.GET, 'applications', params={'page': page, 'unread_only': unread_only})

    def approve_registration_application(self, application_id: int, approve: bool = True,
                                         deny_reason: str | None = None):
        self._logger.debug("LemmyLib approve_registration_application")

        return self.call_api(LemmyApiMethod.PUT, f'admin/registration_application/approve',
                             data={'approve': approve, 'id': application_id, 'deny_reason': deny_reason})

    def purge_person(self, person_id: int, reason: str | None = None):
        self._logger.debug("LemmyLib purge_person")

        return self.call_api(LemmyApiMethod.DELETE, f'admin/person/person',
                             data={'reason': reason, 'person_id': person_id})

    def purge_community(self, community_id: int, reason: str | None = None):
        self._logger.debug("LemmyLib purge_community")

        return self.call_api(LemmyApiMethod.DELETE, f'admin/community/community',
                             data={'reason': reason, 'community_id': community_id})

    def purge_post(self, post_id: int, reason: str | None = None):
        self._logger.debug("LemmyLib purge_post")

        return self.call_api(LemmyApiMethod.DELETE, f'admin/post/post',
                             data={'reason': reason, 'post_id': post_id})

    def purge_comment(self, comment_id: int, reason: str | None = None):
        self._logger.debug("LemmyLib purge_comment")

        return self.call_api(LemmyApiMethod.DELETE, f'admin/comment/comment',
                             data={'reason': reason, 'comment_id': comment_id})

    def get_post(self, post_id: int):
        self._logger.debug("LemmyLib get_post")

        return self.call_api(LemmyApiMethod.GET, f'post', params={'id': post_id})

    def get_comment(self, comment_id: int):
        self._logger.debug("LemmyLib get_comment")

        return self.call_api(LemmyApiMethod.GET, f'comment', params={'id': comment_id})

    def remove_post(self, post_id: int, removed: bool = True, reason: str | None = None):
        self._logger.debug("LemmyLib remove_post")

        return self.call_api(LemmyApiMethod.POST, f'post/remove',
                             data={'reason': reason, 'post_id': post_id, 'removed': removed})

    def remove_comment(self, comment_id: int, removed: bool = True, reason: str | None = None):
        self._logger.debug("LemmyLib remove_comment")

        return self.call_api(LemmyApiMethod.POST, f'comment/remove',
                             data={'reason': reason, 'comment_id': comment_id, 'removed': removed})

    def remove_person(self, person_id: int, removed: bool = True, reason: str | None = None):
        self._logger.debug("LemmyLib remove_person")

        return self.call_api(LemmyApiMethod.POST, f'person/remove',
                             data={'reason': reason, 'person_id': person_id, 'removed': removed})


if __name__ == '__main__':
    print("This is a library, not a script.")
