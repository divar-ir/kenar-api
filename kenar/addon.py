from enum import Enum
from logging import log
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
        return  [w.serialize_model() for w in widgets]


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
    service_type: str = None


class AddonMetaData(BaseModel):
    id: str
    app: App

    created_at: str
    last_modified: str
    status: str


class PostAddon(BaseModel):
    meta_data: AddonMetaData

    token: str

    score: int

    semantic: Dict[str, str] = None
    semantic_sensitives: List[str] = None

    class Config:
        exclude= {"semantic_sensitives"}


   


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
    cost: Optional[int] = None

    @field_validator("cost", mode="before")
    @classmethod
    def set_cost_from_verification(cls, cost: Optional[int], values):
        if cost is None and values.get("verification_cost") is not None:
            return values.get("verification_cost")
        return cost

    class Config:
        exclude = {"verification_cost", "management_permalink", 
                   "notes", "removal_permalink", "semantic_sensitives"}

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        p = [w.serialize_model() for w in widgets]
        return p


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
        return [
            get_widget_class(w.keys()).deserialize_model(w) for w in widgets
        ]

    @field_serializer("widgets")
    def serialize_widgets(self, widgets, _info):
        if widgets:
            p = [w.serialize_model() for w in widgets]
            return p
        return None


class GetUserAddonsResponse(BaseModel):
    addons: List[UserAddon] = None
