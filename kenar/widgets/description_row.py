from typing import Dict

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from kenar.widgets.base import BaseWidget


class DescriptionRow(BaseModel, BaseWidget):
    text: str
    has_divider: bool = False
    is_primary: bool = False
    expandable: bool = False
    padded: bool = False
    preview_max_line: int = 0

    @model_validator(mode="after")
    def check_preview_max_line(self) -> Self:
        expandable_ = self.expandable
        preview_max_line_ = self.preview_max_line
        if expandable_ is False and preview_max_line_ > 0:
            raise ValueError(
                "Can not set preview_max_line when field expandable is set to False"
            )
        return self

    def serialize_model(self) -> dict:
        return {
            "description_row": self.model_dump(exclude={"is_primary", "padded"}),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("description_row", {})
        return cls.model_validate(widget_data)
