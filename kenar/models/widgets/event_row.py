from typing import Dict

from pydantic import BaseModel, model_validator

from pydantic import BaseModel

from kenar.models.icons import Icon
from kenar.models.widgets.action import get_action, get_link_from_action


class EventRow(BaseModel):
    title: str
    subtitle: str = ''
    has_indicator: bool = False
    image_url: str = ''
    label: str = ''
    has_divider: bool = False
    link: str = ''
    padded: bool = False
    icon: Icon

    def serialize_model(self) -> dict:
        return {
            "widget_type": "EVENT_ROW",
            "data": {"@type": "type.googleapis.com/widgets.EventRowData"} |
            self.dict(exclude={'link'}) |
            get_action(link=self.link)
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get('data', {})
        widget_data.pop('@type', None)
        if 'action' in widget_data:
            widget_data['link'] = get_link_from_action(widget_data['action'])
            widget_data.pop('action', None)
        return cls.parse_obj(widget_data)
