from typing import Dict

from pydantic import model_serializer, BaseModel, field_validator, model_validator
from pydantic.v1 import root_validator

from kenar.models.icons import Icon
from kenar.models.widgets.color import Color


class EvaluationRow(BaseModel):
    class Section(BaseModel):
        text: str
        text_color: Color
        section_color: Color

    indicator_text: str

    indicator_percentage: int
    indicator_icon: Icon

    indicator_color: Color

    left: Section
    middle: Section
    right: Section

    @field_validator('indicator_percentage')
    @classmethod
    def check_indicator_percentage(cls, indicator_percentage: int) -> int:
        if indicator_percentage < 0 or indicator_percentage > 100:
            raise ValueError('Field indicator_percentage should be in range [0,100]')
        return indicator_percentage

    def serialize_model(self) -> dict:
        return {
            "widget_type": "EVALUATION_ROW",
            "data": {"@type": "type.googleapis.com/widgets.EvaluationRowData"} |
                    self.model_dump()
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get('data', {})
        widget_data.pop('@type', None)
        return cls.parse_obj(widget_data)
