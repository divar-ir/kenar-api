from typing import Dict


class Semantics:
    def __init__(self):
        self._semantics: Dict[str, str] = {}
        self._sensitives = []

    def add(self, key: str, value: str):
        if key in self._semantics:
            raise ValueError(f"attempt to add duplicate key to semantics: {key}")
        if type(key) is not str:
            raise TypeError(f"key must be a string")
        if type(value) is not str:
            raise TypeError(f"value must be a string")

        self._semantics[key] = value

    def add_sensitive(self, key: str, value: str):
        self.add(key, value)
        if key not in self._sensitives:
            self._sensitives.append(key)

    def pack(self):
        return {
            "semantic": self._semantics,
            "semantic_sensitives": self._sensitives
        }
