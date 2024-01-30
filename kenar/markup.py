from typing import Dict


class Markup:
    def __init__(self, label: str, params: Dict[str, str]):
        self._label = label
        self._params = params

    def pack(self):
        return {
            "action": "LINK",
            "data": {
                "caption": self._label,
                "extra_data": self._params,
            }
        }
