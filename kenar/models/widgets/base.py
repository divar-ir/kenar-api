import abc
from typing import Dict


class BaseWidget:
    @abc.abstractmethod
    def serialize_model(self) -> Dict:
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize_model(cls, data: Dict) -> object:
        pass
