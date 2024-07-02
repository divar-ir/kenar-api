from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BotButton(BaseModel):
    class Action(Enum):
        LINK = "LINK"
        DIRECT_LINK = "DIRECT_LINK"

    class ButtonData(BaseModel):
        icon_name: str
        extra_data: dict = {}
        caption: str
        direct_link: str

    data: ButtonData
    action: Action


class SetNotifyChatPostConversationsRequest(BaseModel):
    post_token: str
    endpoint: str
    identification_key: str


class SetNotifyChatPostConversationsResponse(BaseModel):
    pass


class SendMessageV2Request(BaseModel):
    user_id: str
    peer_id: str
    post_token: str
    type: str = "TEXT"
    message: str
    sender_btn: Optional[BotButton]
    receiver_btn: Optional[BotButton]


class SendMessageV2Response(BaseModel):
    status: int
    message: str


class PostConversationsNotificationRegisterPayload(BaseModel):
    post_token: str
    phone: str = None
    endpoint: str


class PostConversationsNotificationPayload(BaseModel):
    registration_payload: PostConversationsNotificationRegisterPayload
    identification_key: str
