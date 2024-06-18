from enum import Enum

import httpx
from pydantic import BaseModel

from kenar.api_client.request import mask_secret, _request
from kenar.errors import HTTPException, APIException


class BotButton(BaseModel):
    class Action(Enum):
        LINK = 'LINK'
        DIRECT_LINK = 'DIRECT_LINK'

    class ButtonData(BaseModel):
        icon_name: str
        extra_data: dict= {}
        caption: str
        direct_link: str

    data: ButtonData
    action: Action


class SetNotifyChatPostConversationsRequest(BaseModel):
    post_token: str
    endpoint: str
    identification_key: str


class SendMessageV2Request(BaseModel):
    user_id: str
    peer_id: str
    post_token: str
    type: str = 'TEXT'
    message: str
    sender_btn: BotButton
    receiver_btn: BotButton


def set_notify_chat_post_conversations(client: httpx.Client, data: SetNotifyChatPostConversationsRequest):
    return _request(client=client, url='https://api.divar.ir/v1/open-platform/notify/chat/post-conversations',
                    data=data, method='POST')


def send_message(client: httpx.Client, data: SendMessageV2Request):
    return _request(client=client, url='https://api.divar.ir/v2/open-platform/chat/conversation',
                    data=data, method='POST')
