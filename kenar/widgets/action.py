from typing import Dict


def get_action(link: str) -> Dict:
    return (
        {
            "action": {
                "type": "LOAD_WEB_VIEW_PAGE",
                "fallback_link": link,
                "payload": {
                    "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                    "url": link,
                },
            }
        }
        if len(link) > 0
        else {}
    )


def get_link_from_action(action: Dict) -> str:
    return action["payload"]["url"]
