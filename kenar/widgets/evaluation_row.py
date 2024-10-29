from typing import Dict

from pydantic import BaseModel, field_validator

from kenar.icons import Icon, IconName
from kenar.widgets.base import BaseWidget
from kenar.widgets.color import Color


class EvaluationRow(BaseModel, BaseWidget):
    class Section(BaseModel):
        text: str
        text_color: Color = Color.COLOR_UNSPECIFIED
        section_color: Color

        class Config:
            exclude = {"text_color"}


    indicator_text: str

    indicator_percentage: int
    indicator_icon: Icon = Icon(icon_name=IconName.UNKNOWN)

    indicator_color: Color = Color.COLOR_UNSPECIFIED

    left: Section
    middle: Section
    right: Section

    @field_validator("indicator_percentage")
    @classmethod
    def check_indicator_percentage(cls, indicator_percentage: int) -> int:
        if indicator_percentage < 0 or indicator_percentage > 100:
            raise ValueError("Field indicator_percentage should be in range [0,100]")
        return indicator_percentage

    def serialize_model(self) -> dict:
        return {
            "evaluation_row": self.model_dump(exclude={"indicator_color", "indicator_icon"}) 
            | self.indicator_icon.model_dump() ,
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("evaluation_row", {})

        widget_data["icon"] = {
            "icon_name": "UNKNOWN"
        }
        return cls.model_validate(widget_data)
