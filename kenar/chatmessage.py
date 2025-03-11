from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from kenar.icons import IconName
from kenar.widgets.action import Action


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


class ChatButton(BaseModel):
    action: Action
    caption: str
    icon: IconName


class ChatButtonRow(BaseModel):
    buttons: List[ChatButton] = Field(default_factory=list)


class ChatButtonGrid(BaseModel):
    rows: List[ChatButtonRow] = Field(default_factory=list)


class ChatBotSendMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    text_message: str
    media_token: Optional[str] = None
    buttons: Optional[ChatButtonGrid] = None


class ChatBotSendMessageResponse(BaseModel):
    pass
