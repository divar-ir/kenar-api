from typing import Optional


class BotButton:
    def __init__(self, caption: str, direct_link: str = "", extra_data: dict = None):
        if direct_link and extra_data:
            raise ValueError("Only one of direct_link or extra_data should be provided.")
        if not direct_link and not extra_data:
            raise ValueError("Either direct_link or extra_data should be provided.")

        self.caption = caption
        self.direct_link = direct_link
        self.extra_data = extra_data

    def as_dict(self):
        if self.extra_data:
            return {
                "action": "LINK",
                "data": {
                    "caption": self.caption,
                    "extra_data": self.extra_data,
                },
            }
        else:
            return {
                "action": "DIRECT_LINK",
                "data": {
                    "caption": self.caption,
                    "direct_link": self.direct_link,
                },
            }


class SendMessageRequest:
    user_id: str
    peer_id: str
    post_token: str
    message: str
    sender_btn: Optional[BotButton]
    receiver_btn: Optional[BotButton]

    def __init__(self, user_id: str, peer_id: str, post_token: str, message: str,
                 sender_btn: BotButton = None, receiver_btn: BotButton = None):
        self.user_id = user_id
        self.peer_id = peer_id
        self.post_token = post_token
        self.message = message
        self.sender_btn = sender_btn
        self.receiver_btn = receiver_btn

    def as_dict(self):
        d = {
            "user_id": self.user_id,
            "peer_id": self.peer_id,
            "post_token": self.post_token,
            "type": "TEXT",
            "message": self.message,
        }

        if self.sender_btn:
            d["sender_btn"] = self.sender_btn.as_dict()

        if self.receiver_btn:
            d["receiver_btn"] = self.receiver_btn.as_dict()
