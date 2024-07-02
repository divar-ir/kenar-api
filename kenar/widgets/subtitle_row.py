from typing import Dict

from pydantic import BaseModel

from kenar.widgets.base import BaseWidget


class SubtitleRow(BaseModel, BaseWidget):
    text: str
    has_divider: bool = False

    def serialize_model(self) -> dict:
        return {
            "widget_type": "SUBTITLE_ROW",
            "data": {"@type": "type.googleapis.com/widgets.SubtitleRowData"}
            | self.dict(),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("data", {})
        widget_data.pop("@type", None)
        return cls.parse_obj(widget_data)
