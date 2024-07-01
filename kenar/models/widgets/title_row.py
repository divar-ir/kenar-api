from typing import Dict

from pydantic import BaseModel, model_validator

from kenar.models.widgets.color import Color


class TitleRow(BaseModel):
    text: str
    text_color: Color = Color.TEXT_PRIMARY

    def serialize_model(self) -> dict:
        return {
            "widget_type": "TITLE_ROW",
            "data": {"@type": "type.googleapis.com/widgets.TitleRowData"} | self.model_dump()
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get('data', {})
        widget_data.pop('@type', None)
        return cls.parse_obj(widget_data)
