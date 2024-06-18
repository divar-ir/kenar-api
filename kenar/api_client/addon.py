from typing import List, Optional, Dict

import httpx
from pydantic import BaseModel, field_serializer

from kenar.api_client.request import _request


class Widget(BaseModel):
    widget_type: str
    data: dict
    # action: Optional[str] = None
    #
    # @field_serializer('action')
    # def serialize_action(self, action: Optional[str], _info):
    #     if action:
    #         return {
    #             "type": "LOAD_WEB_VIEW_PAGE",
    #             "fallback_link": action,
    #             "payload": {
    #                 "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
    #                 "url": action
    #             }
    #         }


class Widgets(BaseModel):
    widget_list: list[Widget]


class CreatePostAddonRequest(BaseModel):
    token: str

    widgets: Widgets
    notes: str = ''
    semantic: Dict[str, str] = {}
    semantic_sensitives: List[str] = []


class CreatePostAddonResponse(BaseModel):
    id: str


class DeletePostAddonRequest(BaseModel):
    token: str


class App(BaseModel):
    slug: str
    display: str
    avatar: str
    status: str
    service_type: str


class AddonMetaData(BaseModel):
    id: str
    app: App

    created_at: int  # google.protobuf.Timestamp
    last_modified: int
    status: str


class PostAddon(BaseModel):
    meta_data: AddonMetaData

    token: str

    widgets: Widgets

    score: int

    semantic: Dict[str, str]
    semantic_sensitives: List[str]


class GetPostAddonsRequest(BaseModel):
    id: str = ''  # TODO: oneof
    token: str = ''


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


def create_user_addon(client: httpx.Client, data: CreateUserAddonRequest) -> CreateUserAddonResponse:
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/user/{data.phone}', 'POST', data)


def delete_user_addon(client: httpx.Client, data: DeleteUserAddonRequest):
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/user/{data.id}', 'DELETE', data)


def get_user_addons(client: httpx.Client, data: GetUserAddonsRequest) -> GetUserAddonsResponse:
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/user/{data.phone}', 'GET', data)


def create_post_addon(client: httpx.Client, data: CreatePostAddonRequest) -> CreatePostAddonResponse:
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/post/{data.token}', 'POST', data)


def delete_post_addon(client: httpx.Client, data: DeletePostAddonRequest):
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/post/{data.token}', 'DELETE', data)


def get_post_addons(client: httpx.Client, data: GetPostAddonsRequest) -> GetPostAddonsResponse:
    return _request(client, f'https://api.divar.ir/v1/open-platform/addons/post/{data.token}', 'GET', data)


