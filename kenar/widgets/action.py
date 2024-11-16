from typing import Dict


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
