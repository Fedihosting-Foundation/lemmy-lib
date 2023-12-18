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


class LemmyPostSort(Enum):
    HOT = 'Hot'
    ACTIVE = 'Active'
    NEW = 'New'
    OLD = 'Old'
    TOP = 'Top'
    CONTROVERSIAL = 'Controversial'
    MOSTCOMMENTS = 'MostComments'
    NEWCOMMENTS = 'NewComments'


class LemmyListingType(Enum):
    ALL = 'All'
    LOCAL = 'Local'
    SUBSCRIBED = 'Subscribed'


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

    def get_session(self, other_headers: None | dict = None):
        if other_headers is None:
            other_headers = {}
        session = requests.Session()
        session.cookies.set('jwt', self.get_jwt())
        session.headers.update({**self.get_headers(), **other_headers})
        return session

    def call_api(self, method: LemmyApiMethod, endpoint: str, params: dict = None, headers: dict = None,
                 data: dict = None):
        self._logger.debug("LemmyLib call_api")
        if headers is None:
            headers = self.get_headers()
        if params is None:
            params = {}
        else:
            for key, value in params.copy().items():
                print(value)
                print(type(value))
                if value is None:
                    params.pop(key)
                if isinstance(value, bool):
                    params[key] = str(value).lower()

        if self._url is None:
            raise Exception("LemmyLib: URL not set")

        url = f'{self._url}{self.get_base_path()}{endpoint}'

        self._logger.debug(f"LemmyLib call_api: {method} {url}")
        with self.get_session(headers) as session:
            if method == LemmyApiMethod.GET:
                response = session.get(url, params=params)
            elif method == LemmyApiMethod.POST:
                response = session.post(url, params=params, json=data)
            elif method == LemmyApiMethod.PUT:
                response = session.put(url, params=params, json=data)
            elif method == LemmyApiMethod.DELETE:
                response = session.delete(url, params=params)
            else:
                raise Exception("LemmyLib: Unknown method")

        self._logger.debug(f"LemmyLib call_api: {response.status_code} {response.text}")

        if response.ok:
            return response
        else:
            self._logger.error(f"LemmyLib call_api: "
                               f"{method} {url}"
                               f"{response.status_code} {response.text}")
            return None

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
        response = self.call_api(LemmyApiMethod.POST, 'user/login',
                                 data={'username_or_email': username, 'password': password, 'totp_2fa_token': totp})

        if not only_jwt:
            self.set_jwt(response.json()["jwt"])

        return response

    def list_registration_applications(self, page: int = 1, unread_only: bool = False):
        self._logger.debug("LemmyLib list_registration_applications")

        return self.call_api(LemmyApiMethod.GET, 'admin/registration_application/list',
                             params={'page': page, 'unread_only': unread_only})

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

    def list_comments(self, page: int = 1, post_id: int | None = None, sort: LemmyPostSort = None,
                      listing_type: LemmyListingType = None, parent_id: int | None = None,
                      community_id: int | None = None, community_name: str | None = None, user_id: int | None = None,
                      user_name: str | None = None, saved_only: bool = False):
        self._logger.debug("LemmyLib list_comments")

        if post_id is None and community_id is None and community_name is None and user_id is None and user_name is None:
            raise Exception("LemmyLib: Either post_id, community_id, community_name, user_id or user_name must be set")

        return self.call_api(LemmyApiMethod.GET, f'comments', params={'page': page, 'post_id': post_id, 'sort': sort,
                                                                      'type_': listing_type.value,
                                                                      'parent_id': parent_id,
                                                                      'community_id': community_id,
                                                                      'community_name': community_name,
                                                                      'user_id': user_id,
                                                                      'user_name': user_name,
                                                                      'saved_only': saved_only})

    def list_posts(self,
                   page: int | None = None, page_cursor: int | None = None, sort: LemmyPostSort = None,
                   listing_type: LemmyListingType = None,
                   community_id: int | None = None, community_name: str | None = None,
                   liked_only: bool = False, disliked_only: bool = False,
                   saved_only: bool = False):
        self._logger.debug("LemmyLib list_posts")

        return self.call_api(LemmyApiMethod.GET, f'posts',
                             params={'page_cursor': page_cursor, 'sort': sort, 'type_': listing_type.value,
                                     'community_id': community_id,
                                     'page': page,
                                     'community_name': community_name,
                                     'liked_only': liked_only,
                                     'disliked_only': disliked_only,
                                     'saved_only': saved_only})

    def get_person(self, person_id: int | None = None, username: str | None = None):
        self._logger.debug("LemmyLib get_person")

        if person_id is None and username is None:
            raise Exception("LemmyLib: Either person_id or username must be set")

        return self.call_api(LemmyApiMethod.GET, f'person', params={'person_id': person_id, 'username': username})

    def get_community(self, community_id: int | None = None, name: str | None = None):
        self._logger.debug("LemmyLib get_community")

        if community_id is None and name is None:
            raise Exception("LemmyLib: Either community_id or name must be set")

        return self.call_api(LemmyApiMethod.GET, f'community', params={'id': community_id, 'name': name})

    def remove_post(self, post_id: int, reason: str | None = None, removed: bool = True):
        self._logger.debug("LemmyLib remove_post")

        return self.call_api(LemmyApiMethod.POST, f'post/remove',
                             data={'reason': reason, 'post_id': post_id, 'removed': removed})

    def remove_comment(self, comment_id: int, reason: str | None = None, removed: bool = True):
        self._logger.debug("LemmyLib remove_comment")

        return self.call_api(LemmyApiMethod.POST, f'comment/remove',
                             data={'reason': reason, 'comment_id': comment_id, 'removed': removed})

    def update_comment(self, comment_id: int, content: str):
        self._logger.debug("LemmyLib update_comment")

        return self.call_api(LemmyApiMethod.PUT, f'comment/update',
                             data={'comment_id': comment_id, 'content': content})

    def update_post(self, post_id: int, content: str | None = None, nsfw: bool | None = None,
                    title: str | None = None):
        self._logger.debug("LemmyLib update_post")

        if post_id is None:
            raise Exception("LemmyLib: post_id must be set")

        return self.call_api(LemmyApiMethod.PUT, f'post/update',
                             data={'post_id': post_id, 'content': content, 'nsfw': nsfw, 'title': title})

    def update_person(self, person_id: int, name: str | None = None, display_name: str | None = None,
                      bio: str | None = None, matrix_user_id: str | None = None, avatar: str | None = None,
                      banner: str | None = None, bot_account: bool | None = None):
        """WARNING: This method is ONLY for updating the person's own profile! Or an exception will be thrown.
        """
        self._logger.debug("LemmyLib update_person")

        if person_id is None:
            raise Exception("LemmyLib: person_id must be set")

        return self.call_api(LemmyApiMethod.PUT, f'user/save_user_settings',
                             data={'person_id': person_id, 'name': name, 'display_name': display_name, 'bio': bio,
                                   'matrix_user_id': matrix_user_id, 'avatar': avatar, 'banner': banner,
                                   'bot_account': bot_account})

    def ban_person(self, person_id: int, reason: str | None = None, ban_expires: str | None = None, banned: bool = True,
                   remove_data: bool = False):
        self._logger.debug("LemmyLib ban_person")

        if person_id is None:
            raise Exception("LemmyLib: person_id must be set")

        return self.call_api(LemmyApiMethod.POST, f'user/ban',
                             data={'reason': reason, 'person_id': person_id, 'ban_expires': ban_expires, 'ban': banned,
                                   "remove_data": remove_data})

    def remove_community(self, community_id: int, reason: str | None = None, removed: bool = True):
        self._logger.debug("LemmyLib remove_community")

        return self.call_api(LemmyApiMethod.POST, f'community/remove',
                             data={'reason': reason, 'community_id': community_id, 'removed': removed})

    def remove_person(self, person_id: int, reason: str | None = None, removed: bool = True):
        self._logger.debug("LemmyLib remove_person")

        if person_id is None:
            raise Exception("LemmyLib: person_id must be set")

        return self.call_api(LemmyApiMethod.POST, f'person/remove',
                             data={'reason': reason, 'person_id': person_id, 'removed': removed})


if __name__ == '__main__':
    print("This is a library, not a script.")
