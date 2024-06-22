import base64
import urllib.parse
from typing import List, Optional, Dict

from pydantic import BaseModel

from kenar.api_client.addon import CreateUserAddonRequest, CreateUserAddonResponse, DeleteUserAddonRequest, \
    GetUserAddonsRequest, GetUserAddonsResponse, CreatePostAddonRequest, CreatePostAddonResponse, \
    DeletePostAddonRequest, GetPostAddonsRequest, GetPostAddonsResponse, create_user_addon, delete_user_addon, \
    get_user_addons, create_post_addon, delete_post_addon, get_post_addons
from kenar.api_client.chatmessage import SetNotifyChatPostConversationsRequest, set_notify_chat_post_conversations, \
    SendMessageV2Request, send_message
from kenar.api_client.finder import SearchPostRequest, \
    SearchPostResponse, search_post, GetPostRequest, GetUserRequest, \
    get_post, get_user, GetUserPostsRequest, get_user_posts
from kenar.api_client.oauth import get_access_token, OAuthAccessTokenRequest, AccessTokenResponse, OauthResourceType


class AppConfig(BaseModel):
    app_slug: str
    api_key: str


class AppOauthConfig(BaseModel):
    oauth_secret: str
    oauth_redirect_url: str


class AppChatConfig(BaseModel):
    identification_key: str


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
    def __init__(self, default_headers: Dict):
        self._default_headers = default_headers

    def set_notify_chat_post_conversations(self, access_token: str, data: SetNotifyChatPostConversationsRequest):
        set_notify_chat_post_conversations(data=data,
                                           headers={**self._default_headers, **{'x-access-token': access_token}})

    def send_message(self, access_token: str, message_data: SendMessageV2Request):
        return send_message(data=message_data, headers={**self._default_headers, **{'x-access-token': access_token}})


class FinderService:
    def __init__(self, default_headers: Dict):
        self._default_headers = default_headers

    def search_post(self, data: SearchPostRequest) -> SearchPostResponse:
        return search_post(data, headers=self._default_headers)

    def get_post(self, data: GetPostRequest):
        return get_post(data=data, headers=self._default_headers)

    def get_user(self, access_token: str, data: Optional[GetUserRequest] = None):
        return get_user(data=data, headers={**self._default_headers, **{'x-access-token': access_token}})

    def get_user_posts(self, access_token: str, data: Optional[GetUserPostsRequest] = None):
        return get_user_posts(data=data, headers={**self._default_headers, **{'x-access-token': access_token}})


class AddonService:
    def __init__(self, default_headers: Dict):
        self._default_headers = default_headers

    def create_user_addon(self, access_token: str, data: CreateUserAddonRequest) -> CreateUserAddonResponse:
        return create_user_addon(data=data, headers={**self._default_headers, **{'x-access-token': access_token}})

    def delete_user_addon(self, data: DeleteUserAddonRequest):
        return delete_user_addon(data, headers=self._default_headers)

    def get_user_addons(self, data: GetUserAddonsRequest) -> GetUserAddonsResponse:
        return get_user_addons(data, headers=self._default_headers)

    def create_post_addon(self, access_token: str, data: CreatePostAddonRequest) -> CreatePostAddonResponse:
        return create_post_addon(data=data, headers={**self._default_headers, **{'x-access-token': access_token}})

    def delete_post_addon(self, data: DeletePostAddonRequest):
        return delete_post_addon(data, headers=self._default_headers)

    def get_post_addons(self, data: GetPostAddonsRequest) -> GetPostAddonsResponse:
        return get_post_addons(data, headers=self._default_headers)


class OAuthService:
    def __init__(self, app_slug, oauth_redirect_url, oauth_secret, default_headers: Dict):
        self._app_slug = app_slug
        self._oauth_redirect_url = oauth_redirect_url
        self._oauth_secret = oauth_secret
        self._default_headers = default_headers

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
        return get_access_token(
            headers=self._default_headers | {'Content-Type': 'application/x-www-form-urlencoded'},
            data=OAuthAccessTokenRequest(
                client_id=self._app_slug,
                client_secret=self._oauth_secret,
                code=authorization_token,
                redirect_uri=self._oauth_redirect_url
            )
        )

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

        self.default_headers = {"x-api-key": conf.api_key}
        self.app_config = conf
        self.oauth = None
        self.chat = None

        self.finder = None
        self.addon = None

    def add_chat_service(self, conf: AppChatConfig):
        if not conf.identification_key:
            raise ValueError("the KENAR_IDENT_KEY environment variable must be set")

        self.chat = ChatService(default_headers=self.default_headers)

    def add_oauth_service(self, conf: AppOauthConfig):
        if not conf.oauth_redirect_url:
            raise ValueError("the KENAR_OAUTH_REDIRECT_URL environment variable must be set")
        if not conf.oauth_secret:
            raise ValueError("the KENAR_OAUTH_SECRET environment variable must be set")
        self.oauth = OAuthService(app_slug=self.app_config.app_slug,
                                  oauth_redirect_url=conf.oauth_redirect_url,
                                  oauth_secret=conf.oauth_secret, default_headers=self.default_headers)

    def add_finder_service(self):
        self.finder = FinderService(default_headers=self.default_headers)

    def add_addon_service(self):
        self.addon = AddonService(default_headers=self.default_headers)