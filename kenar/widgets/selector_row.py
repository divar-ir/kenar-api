from typing import Dict

from pydantic import BaseModel

from kenar.icons import Icon
from kenar.widgets.action import get_action, get_link_from_action
from kenar.widgets.base import BaseWidget


class SelectorRow(BaseModel, BaseWidget):
    title: str

    has_divider: bool = False

    has_notification: bool = False
    icon: Icon

    has_arrow: bool = False

    link: str

    def serialize_model(self) -> dict:
        return {
            "widget_type": "SELECTOR_ROW",
            "data": {"@type": "type.googleapis.com/widgets.SelectorRowData"}
            | self.dict(exclude={"link"})
            | {"small": True}
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
