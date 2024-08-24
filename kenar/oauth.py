from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel


class OauthResourceType(str, Enum):
    UNKNOWN = "UNKNOWN"
    POST_ADDON_CREATE = "POST_ADDON_CREATE"
    USER_PHONE = "USER_PHONE"
    USER_ADDON_CREATE = "USER_ADDON_CREATE"
    CHAT_MESSAGE_SEND = "CHAT_MESSAGE_SEND"
    CHAT_CONVERSATION_READ = "CHAT_CONVERSATION_READ"
    USER_POSTS_GET = "USER_POSTS_GET"
    CHAT_POST_CONVERSATIONS_READ = "CHAT_POST_CONVERSATIONS_READ"
    CHAT_POST_CONVERSATIONS_MESSAGE_SEND = "CHAT_POST_CONVERSATIONS_MESSAGE_SEND"
    USER_VERIFICATION_CREATE = "USER_VERIFICATION_CREATE"
    OFFLINE_ACCESS = "OFFLINE_ACCESS"

    MANAGEMENT_APPS_READ = "MANAGEMENT_APPS_READ"
    MANAGEMENT_APPS_WRITE = "MANAGEMENT_APPS_WRITE"

    POST_ONGOING_IMAGES_GET = "POST_ONGOING_IMAGES_GET"


class AccessTokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str

    def __init__(self, access_token: str, token_type: str, expires_in: int, scope: str):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope

    def as_dict(self) -> Dict:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope,
        }


class OAuthAccessTokenRequest:
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

    def __init__(self, client_id: str, client_secret: str, code: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri

    def as_dict(self) -> Dict:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }


class Scope:
    resource_type: OauthResourceType
    resource_id: Optional[str]

    def __init__(self, resource_type: OauthResourceType, resource_id: Optional[str] = None):
        self.resource_type = resource_type
        self.resource_id = resource_id


class SendChatMessageResourceIdParams(BaseModel):
    user_id: str
    post_token: str
    peer_id: str
