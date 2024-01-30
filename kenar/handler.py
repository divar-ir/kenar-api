import abc

from pydantic import BaseModel


class ChatMessagePayloadUser(BaseModel):
    id: str
    is_supply: bool


class ChatMessagePayloadMetadata(BaseModel):
    title: str
    category: str
    post_token: str


class ChatMessageTextData(BaseModel):
    text: str


class ChatMessagePayload(BaseModel):
    id: str
    type: str
    data: ChatMessageTextData
    sender: ChatMessagePayloadUser
    receiver: ChatMessagePayloadUser
    metadata: ChatMessagePayloadMetadata
    sent_at: int


class Notification(BaseModel):
    type: str
    timestamp: int
    payload: ChatMessagePayload


class Handler(abc.ABC):

    @abc.abstractmethod
    def handle(self, notification: Notification):
        raise NotImplemented


class ChatNotificationHandler(Handler):
    def handle(self, notification: Notification):
        match notification.type:
            case "CHAT_MESSAGE":
                self.handle_chat_message(notification.timestamp, notification.payload)

    @abc.abstractmethod
    def handle_chat_message(self, timestamp: int, payload: ChatMessagePayload):
        raise NotImplemented
