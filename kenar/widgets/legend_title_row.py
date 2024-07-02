from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field

from kenar.icons import Icon
from kenar.widgets.base import BaseWidget


class LegendTitleRow(BaseModel, BaseWidget):
    class Tag(BaseModel):
        class BackgroundColor(str, Enum):
            TRANSPARENT = "TRANSPARENT"
            GRAY = "GRAY"
            RED = "RED"

        text: str
        icon: Icon
        bg_color: BackgroundColor

    title: str
    subtitle: str
    has_divider: bool = False
    image_url: str = Field(..., min_length=1)
    tags: List[Tag]

    def serialize_model(self) -> dict:
        return {
            "widget_type": "LEGEND_TITLE_ROW",
            "data": {"@type": "type.googleapis.com/widgets.LegendTitleRowData"}
            | self.dict(),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("data", {})
        widget_data.pop("@type", None)
        return cls.parse_obj(widget_data)
