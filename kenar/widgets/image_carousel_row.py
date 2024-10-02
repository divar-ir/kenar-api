
from typing import List, Dict

from pydantic import BaseModel

from kenar.widgets.base import BaseWidget


class ImageCarouselRow(BaseModel, BaseWidget):
    class ImageCarouselRowItem(BaseModel):
        image_url: str
        description: str

    items: List[ImageCarouselRowItem]
    has_divider: bool = False


    def serialize_model(self) -> dict:
        return {
            "widget_type": "IMAGE_CAROUSEL_ROW",
            "data": {"@type": "type.googleapis.com/widgets.ImageCarouselRowData"} | self.dict(),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("data", {})
        widget_data.pop("@type", None)
        return cls.parse_obj(widget_data)
