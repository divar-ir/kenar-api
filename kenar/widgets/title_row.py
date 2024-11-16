from typing import Dict

from pydantic import BaseModel

from kenar.widgets.base import BaseWidget
from kenar.widgets.color import Color


class TitleRow(BaseModel, BaseWidget):
    text: str
    text_color: Color = Color.COLOR_UNSPECIFIED

    def serialize_model(self) -> dict:
        return {
            "title_row": self.model_dump()
        }

    class Config:
        exclude = {"text_color"}

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("title_row", {})
        return cls.model_validate(widget_data)
