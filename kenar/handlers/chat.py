import abc

from kenar.api_client.chatmessage import SendMessageV2Request
from kenar.bot import PostConversationsNotificationRegisterPayload, \
    PostConversationsNotificationPayload
from kenar.handlers.handler import Handler, Notification


class ChatHandler(Handler):
    def handle(self, notification: Notification):
        pass

    def send_message(self, request: SendMessageV2Request):
        return self.bot.send_message(request=request)

    def register_notify_on_post_conversations(self, notification: PostConversationsNotificationRegisterPayload):
        identification_key = self.generate_identification_key(notification=notification)
        payload = PostConversationsNotificationPayload(
            registration_payload=notification,
            identification_key=identification_key)
        self.store_notification_data(notification=payload)
        self.bot.chat.set_notify_chat_post_conversations(payload)

    @abc.abstractmethod
    def generate_identification_key(self, notification: PostConversationsNotificationRegisterPayload) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def store_notification_data(self, notification: PostConversationsNotificationPayload):
        raise NotImplemented
