from kenar.addons.semantics import Semantics


class PostAddon:
    def __init__(self, post_token: str, widgets, semantics: Semantics):
        self._post_token = post_token
        self._widgets = widgets
        self._semantics = semantics

    def pack(self):
        return {
            "widgets": {
                "widget_list": [
                    w.pack() for w in self._widgets
                ]
            },
            **self._semantics.pack(),
        }
