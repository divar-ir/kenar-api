from typing import Dict


class Markup:
    def __init__(self, label: str, link: str):
        self._label = label
        self._link = link

    def pack(self):
        return {
            "action": "DIRECT_LINK",
            "data": {
                "caption": self._label,
                "direct_link": self._link,
            }
        }
