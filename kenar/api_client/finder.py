from typing import List, Optional

import httpx
from pydantic import BaseModel

from kenar.api_client.request import _request, merge_headers


class SearchPostRequest(BaseModel):
    city: Optional[str]
    districts: Optional[List[str]]
    category: Optional[str]
    query: dict


class SearchPostResponse(BaseModel):
    posts: List[dict]


class GetPostRequest(BaseModel):
    token: str


class GetUserRequest(BaseModel):
    pass


class GetUserPosts(BaseModel):
    pass


def search_post(client: httpx.Client, data: SearchPostRequest) -> SearchPostResponse:
    return _request(client, 'https://api.divar.ir/v1/open-platform/finder/post', 'POST', data)


def get_post(client: httpx.Client, data: GetPostRequest):
    return _request(client, f'https://api.divar.ir/v1/open-platform/finder/post/{data.token}', 'GET', data)


def get_user(client: httpx.Client, data: GetUserRequest):
    return _request(client, f'https://api.divar.ir/v1/open-platform/users', 'POST', data)


def get_user_posts(client: httpx.Client, data: GetUserPosts):
    return _request(client, f'https://api.divar.ir/v1/open-platform/finder/user-posts', 'GET', data)
