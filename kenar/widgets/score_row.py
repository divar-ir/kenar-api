from typing import Optional, Dict

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from kenar.widgets.base import BaseWidget
from kenar.widgets.color import Color
from kenar.widgets.action import get_action, get_link_from_action
from kenar.icons import Icon


class ScoreRow(BaseModel, BaseWidget):
    title: str

    descriptive_score: Optional[str] = None
    percentage_score: Optional[int] = None

    score_color: Color
    link: str
    has_divider: bool = False
    icon: Icon = None

    @model_validator(mode="after")
    def check_score(self) -> Self:
        filled_descriptive_score = (
            self.descriptive_score is not None and len(self.descriptive_score) > 0
        )
        if filled_descriptive_score == bool(self.percentage_score):
            raise ValueError(
                "Exactly one of descriptive_score or percentage_score must be set"
            )
        return self

    def serialize_model(self) -> dict:
        return {
            "widget_type": "SCORE_ROW",
            "data": {"@type": "type.googleapis.com/widgets.ScoreRowData"}
            | self.dict(exclude={"link"})
            | get_action(link=self.link),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("data", {})
        widget_data.pop("@type", None)
        if "action" in widget_data:
            widget_data["link"] = get_link_from_action(widget_data["action"])
            widget_data.pop("action", None)
        return cls.parse_obj(widget_data)
