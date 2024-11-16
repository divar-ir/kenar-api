from typing import Dict


from pydantic import BaseModel

from kenar.icons import Icon, IconName
from kenar.widgets.action import get_action, get_link_from_action
from kenar.widgets.base import BaseWidget


class EventRow(BaseModel, BaseWidget):
    title: str
    subtitle: str = ""
    has_indicator: bool = False
    image_url: str = ""
    label: str = ""
    has_divider: bool = False
    link: str = ""
    padded: bool = False
    icon: Icon = Icon(icon_name=IconName.UNKNOWN)

    def serialize_model(self) -> dict:
        return {
            "event_row": self.model_dump(exclude={"link", "icon", "image_url"})
            | get_action(link=self.link) | {"image_id": self.image_url} | self.icon.model_dump()
        }

    class Config:
        exclude = {"padded", "has_indicator"}

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("event_row", {})
        if "action" in widget_data:
            widget_data["link"] = get_link_from_action(widget_data["action"])
            widget_data.pop("action", None)
        widget_data["image_url"] = widget_data.pop("image_id", "")

        widget_data["icon"] = {
                "icon_name": widget_data.pop("icon_name", "UNKNOWN")
        }

        return cls.model_validate(widget_data)
