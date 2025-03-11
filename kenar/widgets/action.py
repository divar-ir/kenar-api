from typing import Dict, Optional

from pydantic import BaseModel


def get_action(link: str) -> Dict:
    return (
        {
            "action": {
                "open_direct_link": link,
            }
        }
        if len(link) > 0
        else {}
    )


def get_link_from_action(action: Dict) -> str:
    return action.get("open_direct_link", "")


class OpenServerLink(BaseModel):
    data: dict


class Action(BaseModel):
    open_direct_link: Optional[str] = None
    open_server_link: Optional[OpenServerLink] = None
