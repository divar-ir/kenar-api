from enum import Enum
from typing import Dict

from pydantic import BaseModel

from kenar.api_client.request import _request


class BotButton(BaseModel):
    class Action(Enum):
        LINK = 'LINK'
        DIRECT_LINK = 'DIRECT_LINK'

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
    type: str = 'TEXT'
    message: str
    sender_btn: BotButton
    receiver_btn: BotButton


class SendMessageV2Response(BaseModel):
    status: int
    message: str


def set_notify_chat_post_conversations(data: SetNotifyChatPostConversationsRequest,
                                       headers: Dict) -> SetNotifyChatPostConversationsResponse:
    _request(path='/v1/open-platform/notify/chat/post-conversations',
             data=data, method='POST', headers=headers)
    return SetNotifyChatPostConversationsResponse()


def send_message(data: SendMessageV2Request, headers: Dict) -> SendMessageV2Response:
    return SendMessageV2Response(**_request(path='/v2/open-platform/chat/conversation',
                                            data=data, method='POST', headers=headers).json())
