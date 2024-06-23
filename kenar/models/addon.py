from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, model_serializer
from pydantic.v1 import root_validator


class Widget(BaseModel):
    widget_type: str
    data: dict


class Widgets(BaseModel):
    widget_list: List[Widget] = None


class CreatePostAddonRequest(BaseModel):
    token: str

    widgets: Widgets
    notes: str = ''
    semantic: Dict[str, str] = {}
    semantic_sensitives: List[str] = []


class CreatePostAddonResponse(BaseModel):
    pass


class DeletePostAddonRequest(BaseModel):
    token: str


class DeletePostAddonResponse(BaseModel):
    pass


class Status(BaseModel):
    class Status(str, Enum):
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'
        SUSPENDED = 'SUSPENDED'
        DEVELOPMENT = 'DEVELOPMENT'

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

    widgets: Widgets

    score: int

    semantic: Dict[str, str] = None
    semantic_sensitives: List[str] = None


class GetPostAddonsRequest(BaseModel):
    id: str = None
    token: str = None

    @root_validator(pre=True)
    def check_mutually_exclusive(self, values):
        id_, token_ = values.get('id'), values.get('token')
        if id_ and token_:
            raise ValueError('id and token are mutually exclusive.')
        if not id_ and not token_:
            raise ValueError('One of id or token must be set.')
        return values

    @model_serializer
    def ser_model(self) -> dict:
        return {'id': self.id} if self.id is not None else {'token': self.token}


class GetPostAddonsResponse(BaseModel):
    addons: List[PostAddon] = None


class CreateUserAddonRequest(BaseModel):
    widgets: Widgets

    semantic: Dict[str, str] = {}
    semantic_sensitives: List[str] = []
    notes: str = ''
    phone: str
    management_permalink: str = ''
    removal_permalink: str = ''
    categories: List[str]
    ticket_uuid: Optional[str] = None
    verification_cost: Optional[int] = None


class CreateUserAddonResponse(BaseModel):
    id: str


class DeleteUserAddonRequest(BaseModel):
    id: str


class DeletePostAddonResponse(BaseModel):
    pass


class DeleteUserAddonResponse(BaseModel):
    pass


class GetUserAddonsRequest(BaseModel):
    phone: str


class UserAddonFilters(BaseModel):
    categories: List[str]


class UserAddon(BaseModel):
    meta_data: AddonMetaData
    phone: str
    widgets: Widgets

    semantic: Dict[str, str] = {}

    filters: UserAddonFilters


class GetUserAddonsResponse(BaseModel):
    addons: List[UserAddon] = None
