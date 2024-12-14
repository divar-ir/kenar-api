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
    OFFLINE_ACCESS = "offline_access"

    MANAGEMENT_APPS_READ = "MANAGEMENT_APPS_READ"
    MANAGEMENT_APPS_WRITE = "MANAGEMENT_APPS_WRITE"

    POST_ONGOING_IMAGES_GET = "POST_ONGOING_IMAGES_GET"

    BUSINESS_ADDON_CREATE = "BUSINESS_ADDON_CREATE"


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: int
    scope: str


class OAuthAccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

    def dict(self, *args, **kwargs) -> Dict:
        object_dict = super().dict(*args, **kwargs)
        object_dict["grant_type"] = "authorization_code"

        return object_dict


class Scope(BaseModel):
    resource_type: OauthResourceType
    resource_id: Optional[str] = None


class SendChatMessageResourceIdParams(BaseModel):
    user_id: str
    post_token: str
    peer_id: str
