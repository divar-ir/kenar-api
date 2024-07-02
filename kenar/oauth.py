from enum import Enum
from typing import Dict

from pydantic import BaseModel


class OauthResourceType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    POST_ADDON_CREATE = 'POST_ADDON_CREATE'
    USER_PHONE = 'USER_PHONE'
    USER_ADDON_CREATE = 'USER_ADDON_CREATE'
    CHAT_MESSAGE_SEND = 'CHAT_MESSAGE_SEND'
    CHAT_CONVERSATION_READ = 'CHAT_CONVERSATION_READ'
    USER_POSTS_GET = 'USER_POSTS_GET'
    CHAT_POST_CONVERSATIONS_READ = 'CHAT_POST_CONVERSATIONS_READ'
    CHAT_POST_CONVERSATIONS_MESSAGE_SEND = 'CHAT_POST_CONVERSATIONS_MESSAGE_SEND'
    USER_VERIFICATION_CREATE = 'USER_VERIFICATION_CREATE'
    OFFLINE_ACCESS = 'OFFLINE_ACCESS'

    MANAGEMENT_APPS_READ = 'MANAGEMENT_APPS_READ'
    MANAGEMENT_APPS_WRITE = 'MANAGEMENT_APPS_WRITE'

    POST_ONGOING_IMAGES_GET = 'POST_ONGOING_IMAGES_GET'


class AccessTokenResponse(BaseModel):
    access_token: str
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
        object_dict['grant_type'] = 'authorization_code'

        return object_dict
