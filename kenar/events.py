from dataclasses import field
from enum import Enum
from typing import Any, Dict
from typing import Optional

from pydantic import BaseModel


class RegisterEventSubscriptionRequest(BaseModel):
    class EventType(Enum):
        UNKNOWN = 'UNKNOWN'
        NEW_MESSAGE_ON_POST = 'NEW_MESSAGE_ON_POST'

    event_type: EventType
    event_resource_id: Optional[str] = field(default="")
    metadata: Optional[Dict[str, Any]] = field(default=None)


class RegisterEventSubscriptionResponse(BaseModel):
    pass
