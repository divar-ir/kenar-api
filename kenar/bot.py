import json
import logging
from typing import Optional, List

import httpx
from gunicorn.http.body import Body

from kenar.conversation import Conversation
from kenar.errors import IdentificationKeyError, SendBotMessageError
from kenar.botmessage import BotMessage
from kenar.handler import Handler, Notification

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, api_key: str, identification_key: str = ""):
        if not api_key:
            raise ValueError("please provide api-key")
        if not identification_key:
            raise ValueError("please provide identification key")

        self._api_key: str = api_key
        self._identification_key: str = identification_key
        self._handlers: List[Handler] = []

        self._client = httpx.Client(
            headers={"x-api-key": self._api_key},
            base_url="https://api.divar.ir",
        )

    def add_handler(self, handler):
        if self._identification_key == "":
            raise IdentificationKeyError("identification key required")

        self._handlers.append(handler)
        handler.register(self)

    def send_bot_message(self, user_id: str, message: BotMessage):
        data = message.pack()
        data["user_id"] = user_id

        s = json.dumps(data)
        resp = self._client.post(
            url="https://api.divar.ir/v1/open-platform/bot/send-message",
            content=s,
        )

        if resp.status_code != httpx.codes.OK:
            raise SendBotMessageError({"code": resp.status_code, "message": resp.text})

        return

    def send_message(self, conversation: Conversation, message: BotMessage):
        raise NotImplemented

    def attach_addon(self, post_token: str, addon):
        raise NotImplemented

    def attach_user_addon(self, phone_number: str, user_addon):
        raise NotImplemented

    def get_post(self, post_token: str):
        raise NotImplemented

    def find_post(self, query):
        raise NotImplemented

    def __call__(self, environ, start_response):
        identification_key = environ.get("HTTP_AUTHORIZATION")
        if identification_key != self._identification_key:
            start_response("401 Unauthorized", [])
            return iter([])

        body: Optional[Body] = environ.get("wsgi.input")
        if not body:
            return

        logger.info("notification received", extra={"contents": body})

        contents = json.load(body)
        notification = Notification.parse_obj(contents)

        for hnd in self._handlers:
            hnd.handle(notification)

        data = b"{}\n"
        start_response("200 OK", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data])
