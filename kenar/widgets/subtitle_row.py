from typing import Dict

from pydantic import BaseModel

from kenar.widgets.base import BaseWidget


class SubtitleRow(BaseModel, BaseWidget):
    text: str
    has_divider: bool = False

    def serialize_model(self) -> dict:
        return {
            "subtitle_row": self.model_dump()
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("subtitle_row", {})
        return cls.model_validate(widget_data)
