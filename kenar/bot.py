import base64
import logging
import urllib.parse
from typing import List, Optional

import httpx
from pydantic import BaseModel

from kenar.api_client.addon import CreateUserAddonRequest, CreateUserAddonResponse, DeleteUserAddonRequest, \
    GetUserAddonsRequest, GetUserAddonsResponse, CreatePostAddonRequest, CreatePostAddonResponse, \
    DeletePostAddonRequest, GetPostAddonsRequest, GetPostAddonsResponse, create_user_addon, delete_user_addon, \
    get_user_addons, create_post_addon, delete_post_addon, get_post_addons
from kenar.api_client.chatmessage import SetNotifyChatPostConversationsRequest, set_notify_chat_post_conversations, \
    SendMessageV2Request, send_message
from kenar.api_client.finder import SearchPostRequest, SearchPostResponse, search_post, GetPostRequest, GetUserRequest, \
    get_post, get_user, GetUserPosts, get_user_posts
from kenar.api_client.oauth import get_access_token, OAuthAccessTokenRequest, AccessTokenResponse

logger = logging.getLogger(__name__)


class AppConfig(BaseModel):
    app_slug: str
    api_key: str
    oauth_redirect_url: str
    identification_key: str
    oauth_secret: str


class PostConversationsNotificationRegisterPayload(BaseModel):
    post_token: str
    phone: str = None
    endpoint: str


class PostConversationsNotificationPayload(BaseModel):
    registration_payload: PostConversationsNotificationRegisterPayload
    identification_key: str


class Scope(BaseModel):
    scope: str
    resource_id: Optional[str] = None


class SendChatMessageResourceIdParams(BaseModel):
    user_id: str
    post_token: str
    peer_id: str


class ChatModule:
    def __init__(self, client, app_slug):
        self._client = client
        self._app_slug = app_slug

    def set_notify_chat_post_conversations(self, access_token: str, data: SetNotifyChatPostConversationsRequest):
        self._client.headers['x-access-token'] = access_token
        set_notify_chat_post_conversations(client=self._client, data=data)

    def send_message(self, access_token: str, message_data: SendMessageV2Request):
        self._client.headers['x-access-token'] = access_token
        return send_message(self._client, message_data)


class FinderModule:
    def __init__(self, client: httpx.Client, app_slug):
        self._client = client
        self._app_slug = app_slug

    def search_post(self, data: SearchPostRequest) -> SearchPostResponse:
        return search_post(self._client, data)

    def get_post(self, data: GetPostRequest):
        return get_post(self._client, data)

    def get_user(self, access_token: str, data: GetUserRequest):
        self._client.headers['x-access-token'] = access_token
        return get_user(self._client, data)

    def get_user_posts(self, access_token: str, data: Optional[GetUserPosts] = None):
        self._client.headers['x-access-token'] = access_token
        return get_user_posts(self._client, data)


class AddonModule:
    def __init__(self, client, app_slug):
        self._client = client
        self.app_slug = app_slug

    def create_user_addon(self, access_token: str, data: CreateUserAddonRequest) -> CreateUserAddonResponse:
        self._client.headers['x-access-token'] = access_token
        return create_user_addon(self._client, data)

    def delete_user_addon(self, data: DeleteUserAddonRequest):
        return delete_user_addon(self._client, data)

    def get_user_addons(self, data: GetUserAddonsRequest) -> GetUserAddonsResponse:
        return get_user_addons(self._client, data)

    def create_post_addon(self, access_token: str, data: CreatePostAddonRequest) -> CreatePostAddonResponse:
        self._client.headers['x-access-token'] = access_token
        return create_post_addon(self._client, data)

    def delete_post_addon(self, data: DeletePostAddonRequest):
        return delete_post_addon(self._client, data)

    def get_post_addons(self, data: GetPostAddonsRequest) -> GetPostAddonsResponse:
        return get_post_addons(self._client, data)


class OAuthModule:
    def __init__(self, client, app_slug, api_key, oauth_redirect_url, oauth_secret):
        self._client = client
        self._app_slug = app_slug
        self._api_key = api_key
        self._oauth_redirect_url = oauth_redirect_url
        self._oauth_secret = oauth_secret

    def get_oauth_redirect(self, scopes: List[Scope], state: str) -> str:
        oauth_redirect_url_encoded = urllib.parse.quote_plus(self._oauth_redirect_url)
        scope = [f'{scope.scope}.{scope.resource_id}' if scope.resource_id is not None else scope.scope for scope in
                 scopes]
        return f'https://api.divar.ir/oauth2/auth?response_type=code&client_id={self._app_slug}' \
               f'&state={state}&redirect_uri={oauth_redirect_url_encoded}&scope={scope}'

    def get_access_token(self, authorization_token: str) -> AccessTokenResponse:
        return get_access_token(
            client=self._client,
            data=OAuthAccessTokenRequest(
                client_id=self._app_slug,
                client_secret=self._api_key,
                code=authorization_token,
                redirect_uri=self._oauth_secret
            )
        )

    @staticmethod
    def get_send_message_resource_id(params: SendChatMessageResourceIdParams) -> str:
        return base64.b64encode(f'{params.user_id}:{params.post_token}:{params.peer_id}'.encode('utf-8')).decode(
            "utf-8")


class BaseBot:
    def __init__(self, conf: AppConfig):
        if not conf.api_key:
            raise ValueError("please provide api-key")
        if not conf.identification_key:
            raise ValueError("please provide identification key")

        self._api_key: str = conf.api_key
        self._identification_key: str = conf.identification_key

        _client = httpx.Client(
            headers={"x-api-key": self._api_key, 'x-debug-token': 'GhmzEGIR'},
            base_url="https://api.divar.ir",
        )
        self.oauth = OAuthModule(client=_client,
                                 app_slug=conf.app_slug,
                                 api_key=conf.api_key,
                                 oauth_redirect_url=conf.oauth_redirect_url,
                                 oauth_secret=conf.oauth_secret)
        self.chat = ChatModule(client=_client, app_slug=conf.app_slug)

        self.finder = FinderModule(client=_client, app_slug=conf.app_slug)
        self.addon = AddonModule(client=_client, app_slug=conf.app_slug)
