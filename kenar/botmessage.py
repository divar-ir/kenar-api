from typing import Iterable

from kenar.markup import Markup


class BotMessage:
    def __init__(self, text: str, markups: Iterable[Markup] = None):
        self._text = text
        self._markups = markups or []

    def pack(self):
        r = {
            "type": "TEXT",
            "message": self._text,
        }

        if self._markups:
            r["buttons"] = list(map(lambda mk: mk.pack(), self._markups))

        return r
