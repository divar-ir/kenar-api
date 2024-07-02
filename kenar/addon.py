from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, model_serializer, field_serializer, field_validator
from pydantic.v1 import root_validator

from kenar.widgets.widget_type import get_widget_class, WidgetTypesUnion


class CreatePostAddonRequest(BaseModel):
    token: str

    widgets: List[WidgetTypesUnion]
    notes: str = ""
    semantic: Dict[str, str] = {}
    semantic_sensitives: List[str] = []

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        return {"widget_list": [w.serialize_model() for w in widgets]}


class CreatePostAddonResponse(BaseModel):
    pass


class DeletePostAddonRequest(BaseModel):
    token: str


class DeletePostAddonResponse(BaseModel):
    pass


class Status(BaseModel):
    class Status(str, Enum):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        SUSPENDED = "SUSPENDED"
        DEVELOPMENT = "DEVELOPMENT"

    status: Status


class App(BaseModel):
    slug: str
    display: str = None
    avatar: str = None
    status: Status = None
    service_type: str


class AddonMetaData(BaseModel):
    id: str
    app: App

    created_at: str
    last_modified: str
    status: str


class PostAddon(BaseModel):
    meta_data: AddonMetaData

    token: str

    widgets: List[WidgetTypesUnion] = None

    score: int

    semantic: Dict[str, str] = None
    semantic_sensitives: List[str] = None

    @field_validator("widgets", mode="before")
    @classmethod
    def deserialize_model(cls, widgets: Dict):
        widget_list = widgets.get("widget_list", [])
        return [
            get_widget_class(w["widget_type"]).deserialize_model(w) for w in widget_list
        ]

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        if widgets:
            p = [w.serialize_model() for w in widgets]
            return {"widget_list": p}
        return None


class GetPostAddonsRequest(BaseModel):
    id: str = None
    token: str = None

    @root_validator(pre=True)
    def check_mutually_exclusive(self, values):
        id_, token_ = values.get("id"), values.get("token")
        if id_ and token_:
            raise ValueError("id and token are mutually exclusive.")
        if not id_ and not token_:
            raise ValueError("One of id or token must be set.")
        return values

    @model_serializer
    def ser_model(self) -> dict:
        return {"id": self.id} if self.id is not None else {"token": self.token}


class GetPostAddonsResponse(BaseModel):
    addons: List[PostAddon] = None


class CreateUserAddonRequest(BaseModel):
    widgets: List[WidgetTypesUnion]

    semantic: Dict[str, str] = {}
    semantic_sensitives: List[str] = []
    notes: str = ""
    phone: str
    management_permalink: str = ""
    removal_permalink: str = ""
    categories: List[str]
    ticket_uuid: Optional[str] = None
    verification_cost: Optional[int] = None

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        p = [w.serialize_model() for w in widgets]
        return {"widget_list": p}


class CreateUserAddonResponse(BaseModel):
    id: str


class DeleteUserAddonRequest(BaseModel):
    id: str


class DeleteUserAddonResponse(BaseModel):
    pass


class GetUserAddonsRequest(BaseModel):
    phone: str


class UserAddonFilters(BaseModel):
    categories: List[str]


class UserAddon(BaseModel):
    meta_data: AddonMetaData
    phone: str
    widgets: List[WidgetTypesUnion] = None

    semantic: Dict[str, str] = {}

    filters: UserAddonFilters

    @field_validator("widgets", mode="before")
    @classmethod
    def deserialize_model(cls, widgets: Dict):
        widget_list = widgets.get("widget_list", [])
        return [
            get_widget_class(w["widget_type"]).deserialize_model(w) for w in widget_list
        ]

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        if widgets:
            p = [w.serialize_model() for w in widgets]
            return {"widget_list": p}
        return None


class GetUserAddonsResponse(BaseModel):
    addons: List[UserAddon] = None
