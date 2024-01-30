from dataclasses import dataclass


@dataclass
class Conversation:
    user_id: str
    peer_id: str
    post_token: str
