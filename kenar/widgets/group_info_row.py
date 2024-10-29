from typing import List, Dict

from pydantic import BaseModel, field_validator

from kenar.widgets.base import BaseWidget


class GroupInfo(BaseModel, BaseWidget):
    class GroupInfoItem(BaseModel):
        title: str
        value: str

    items: List[GroupInfoItem]
    has_divider: bool = False

    @field_validator("items")
    @classmethod
    def check_items_length(cls, items: List[GroupInfoItem]) -> List[GroupInfoItem]:
        if not 1 < len(items) < 4:
            raise ValueError("Number of items in GroupInfo should be 2 or 3")
        return items

    def serialize_model(self) -> dict:
        return {
            "group_info_row": self.model_dump(),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("group_info_row", {})
        return cls.parse_obj(widget_data)
