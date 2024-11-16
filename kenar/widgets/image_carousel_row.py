
from typing import List, Dict

from pydantic import BaseModel

from kenar.widgets.base import BaseWidget


class ImageCarouselRow(BaseModel, BaseWidget):
    class ImageCarouselRowItem(BaseModel):
        image_url: str
        description: str

        def serialize_model(self) -> dict:
            return {
                "image_id" : self.image_url,
                "description": self.description
            }

    items: List[ImageCarouselRowItem]
    has_divider: bool = False


    def serialize_model(self) -> dict:
        return {
            "image_carousel_row": self.model_dump(),
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get("image_carousel_row", {})
        return cls.model_validate(widget_data)
