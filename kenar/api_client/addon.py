from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel
from pydantic.v1 import root_validator

from kenar.api_client.request import _request


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


class GetPostAddonsResponse(BaseModel):
    addons: List[PostAddon]


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
    addons: List[UserAddon]


def create_user_addon(data: CreateUserAddonRequest, headers: Dict) -> CreateUserAddonResponse:
    return CreateUserAddonResponse(
        **_request(f'/v1/open-platform/addons/user/{data.phone}', 'POST', data,
                   headers=headers).json())


def delete_user_addon(data: DeleteUserAddonRequest, headers: Dict) -> DeleteUserAddonResponse:
    return _request(f'/v1/open-platform/addons/user/{data.id}', 'DELETE', data, headers=headers)


def get_user_addons(data: GetUserAddonsRequest, headers: Dict) -> GetUserAddonsResponse:
    return GetUserAddonsResponse(
        **_request(f'/v1/open-platform/addons/user/{data.phone}', 'GET', data,
                   headers=headers).json())


def create_post_addon(data: CreatePostAddonRequest, headers: Dict) -> CreatePostAddonResponse:
    _request(path=f'/v1/open-platform/addons/post/{data.token}', method='POST', data=data,
             headers=headers)
    return CreatePostAddonResponse()


def delete_post_addon(data: DeletePostAddonRequest, headers: Dict) -> DeletePostAddonResponse:
    return _request(f'/v1/open-platform/addons/post/{data.token}', 'DELETE', data, headers=headers)


def get_post_addons(data: GetPostAddonsRequest, headers: Dict) -> GetPostAddonsResponse:
    return GetPostAddonsResponse(
        **_request(f'/v1/open-platform/addons/post/{data.token}', 'GET', data,
                   headers=headers).json())
