import base64
import urllib.parse
from importlib.metadata import version
from typing import List, Optional

import httpx
from pydantic import BaseModel

from kenar.models.addon import CreateUserAddonRequest, CreateUserAddonResponse, DeleteUserAddonRequest, \
    GetUserAddonsRequest, GetUserAddonsResponse, CreatePostAddonRequest, CreatePostAddonResponse, \
    DeletePostAddonRequest, GetPostAddonsRequest, GetPostAddonsResponse, DeletePostAddonResponse
from kenar.models.chatmessage import SetNotifyChatPostConversationsRequest, SendMessageV2Request, SendMessageV2Response, \
    SetNotifyChatPostConversationsResponse
from kenar.models.finder import SearchPostRequest, \
    SearchPostResponse, GetPostRequest, GetUserRequest, \
    GetUserPostsRequest, GetUserResponse, GetUserPostsResponse, GetPostResponse
from kenar.models.oauth import OAuthAccessTokenRequest, AccessTokenResponse, OauthResourceType
from kenar.models.request import retry

ACCESS_TOKEN_HEADER_NAME = 'x-access-token'


class AppConfig(BaseModel):
    app_slug: str
    api_key: str
    oauth_secret: str
    oauth_redirect_url: str


class PostConversationsNotificationRegisterPayload(BaseModel):
    post_token: str
    phone: str = None
    endpoint: str


class PostConversationsNotificationPayload(BaseModel):
    registration_payload: PostConversationsNotificationRegisterPayload
    identification_key: str


class Scope(BaseModel):
    resource_type: OauthResourceType
    resource_id: Optional[str] = None


class SendChatMessageResourceIdParams(BaseModel):
    user_id: str
    post_token: str
    peer_id: str


class ChatService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def set_notify_chat_post_conversations(
            self, access_token: str,
            data: SetNotifyChatPostConversationsRequest,
    ) -> SetNotifyChatPostConversationsResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url='/v1/open-platform/notify/chat/post-conversations',
                content=data.json(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        send_request()
        return SetNotifyChatPostConversationsResponse()

    def send_message(self, access_token: str, data: SendMessageV2Request) -> SendMessageV2Response:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url='/v2/open-platform/chat/conversation',
                content=data.json(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        rsp = send_request()
        return SendMessageV2Response(**rsp.json())


class FinderService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def search_post(self, data: SearchPostRequest) -> SearchPostResponse:
        @retry(max_retries=5, delay=1)
        def send_request():
            return self._client.post(
                url='/v1/open-platform/finder/post',
                content=data.json()
            )

        rsp = send_request()
        return SearchPostResponse(**rsp.json())

    def get_post(self, data: GetPostRequest) -> GetPostResponse:
        @retry(max_retries=5, delay=1)
        def send_request():
            return self._client.request(
                method='GET',
                url=f'/v1/open-platform/finder/post/{data.token}',
                content=data.json(),
            )

        rsp = send_request()
        return GetPostResponse(**rsp.json())

    def get_user(self, access_token: str, data: GetUserRequest = None):
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url='/v1/open-platform/users',
                content=data.json() if data is not None else '',
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        rsp = send_request()
        return GetUserResponse(**rsp.json())

    def get_user_posts(self, access_token: str, data: Optional[GetUserPostsRequest] = None):
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.get(
                url='/v1/open-platform/finder/user-posts',
                params=data.json() if data is not None else '',
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        rsp = send_request()
        return GetUserPostsResponse(**rsp.json())


class AddonService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def create_user_addon(self, access_token: str, data: CreateUserAddonRequest) -> CreateUserAddonResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url=f'/v1/open-platform/addons/user/{data.phone}',
                content=data.json(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        rsp = send_request()
        return CreateUserAddonResponse(**rsp.json())

    def delete_user_addon(self, data: DeleteUserAddonRequest) -> DeletePostAddonResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.delete(
                url=f'/v1/open-platform/addons/user/{data.id}',
                params=data.json(),
            )

        send_request()
        return DeletePostAddonResponse()

    def get_user_addons(self, data: GetUserAddonsRequest) -> GetUserAddonsResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.get(
                url=f'/v1/open-platform/addons/user/{data.phone}',
                params=data.json(),
            )

        rsp = send_request()
        return GetUserAddonsResponse(**rsp.json())

    def create_post_addon(self, access_token: str, data: CreatePostAddonRequest) -> CreatePostAddonResponse:

        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url=f'/v1/open-platform/addons/post/{data.token}',
                content=data.json(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token}
            )

        send_request()
        return CreatePostAddonResponse()

    def delete_post_addon(self, data: DeletePostAddonRequest) -> DeletePostAddonResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.delete(
                url=f'/v1/open-platform/addons/post/{data.token}',
                params=data.json(),
            )

        send_request()
        return DeletePostAddonResponse()

    def get_post_addons(self, data: GetPostAddonsRequest) -> GetPostAddonsResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.get(
                url=f'/v1/open-platform/addons/post/{data.token}',
                params=data.dict(),
            )

        rsp = send_request()
        return GetPostAddonsResponse(**rsp.json())


class OAuthService:
    def __init__(self, client, app_slug, oauth_redirect_url, oauth_secret):
        self._app_slug = app_slug
        self._oauth_redirect_url = oauth_redirect_url
        self._oauth_secret = oauth_secret
        self._client = client

    def get_oauth_redirect(self, scopes: List[Scope], state: str) -> str:
        scope = [f'{scope.resource_type}.{scope.resource_id}' if scope.resource_id is not None else scope.resource_type
                 for scope in
                 scopes]
        return f'https://api.divar.ir/oauth2/auth?response_type=code&' \
               f'client_id={urllib.parse.quote(self._app_slug)}&' \
               f'state={state}&' \
               f'redirect_uri={urllib.parse.quote(self._oauth_redirect_url)}&' \
               f'scope={urllib.parse.quote(" ".join(scope))}'

    def get_access_token(self, authorization_token: str) -> AccessTokenResponse:
        @retry(max_retries=3, delay=1)
        def send_request():
            return self._client.post(
                url='/oauth2/token',
                data=OAuthAccessTokenRequest(
                    client_id=self._app_slug,
                    client_secret=self._oauth_secret,
                    code=authorization_token,
                    redirect_uri=self._oauth_redirect_url
                ).dict(),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

        rsp = send_request()
        return AccessTokenResponse(**rsp.json())

    @staticmethod
    def get_send_message_resource_id(params: SendChatMessageResourceIdParams) -> str:
        return base64.b64encode(f'{params.user_id}:{params.post_token}:{params.peer_id}'.encode('utf-8')).decode(
            "utf-8")


class KenarApp:
    def __init__(self, conf: AppConfig):
        if not conf.api_key:
            raise ValueError("the KENAR_API_KEY environment variable must be set")
        if not conf.app_slug:
            raise ValueError("the KENAR_APP_SLUG environment variable must be set")
        if not conf.oauth_redirect_url:
            raise ValueError("the KENAR_OAUTH_REDIRECT_URL environment variable must be set")
        if not conf.oauth_secret:
            raise ValueError("the KENAR_OAUTH_SECRET environment variable must be set")

        self.app_config = conf

        self._client = httpx.Client(
            timeout=1,
            headers={'KenarDivarSDK-Version': version('Kenar'), 'x-api-key': conf.api_key,
                     'Content-Type': 'application/json'},
            base_url='https://api.divar.ir')
        self._oauth = OAuthService(client=self._client, app_slug=self.app_config.app_slug,
                                   oauth_redirect_url=conf.oauth_redirect_url,
                                   oauth_secret=conf.oauth_secret)
        self._finder = FinderService(self._client)
        self._chat = ChatService(self._client)
        self._addon = AddonService(self._client)

    @property
    def chat(self):
        return self._chat

    @chat.setter
    def chat(self, service: ChatService):
        if not isinstance(service, ChatService):
            raise ValueError("chat must be an instance of ChatService")
        self._chat = service

    @property
    def finder(self):
        return self._finder

    @finder.setter
    def finder(self, service: FinderService):
        if not isinstance(service, FinderService):
            raise ValueError("finder must be an instance of FinderService")
        self._finder = service

    @property
    def addon(self):
        return self._addon

    @addon.setter
    def addon(self, service: AddonService):
        if not isinstance(service, AddonService):
            raise ValueError("addon must be an instance of AddonService")
        self._addon = service

    @property
    def oauth(self):
        return self._oauth

    @oauth.setter
    def oauth(self, service: OAuthService):
        if not isinstance(service, OAuthService):
            raise ValueError("addon must be an instance of OAuthService")
        self._oauth = service
