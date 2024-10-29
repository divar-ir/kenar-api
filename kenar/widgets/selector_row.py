from typing import Dict

from pydantic import BaseModel

from kenar.icons import Icon, IconName
from kenar.widgets.action import get_action, get_link_from_action
from kenar.widgets.base import BaseWidget


class SelectorRow(BaseModel, BaseWidget):
    title: str

    has_divider: bool = False

    has_notification: bool = False
    icon: Icon = Icon(icon_name=IconName.UNKNOWN)

    has_arrow: bool = False

    link: str

    def serialize_model(self) -> dict:
        return {
            "selector_row": self.model_dump(exclude={"link", "icon"})
            | get_action(link=self.link) | self.icon.model_dump(),
        }

    class Config:
        exclude = {"has_arrow"}

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("selector_row", {})
        if "action" in widget_data:
            widget_data["link"] = get_link_from_action(widget_data["action"])
            widget_data.pop("action", None)
        if "icon_name" in widget_data:
            widget_data["icon"] = Icon(icon_name=widget_data.pop("icon_name"))
        return cls.model_validate(widget_data)
