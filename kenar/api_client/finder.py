from typing import List, Optional, Dict

from pydantic import BaseModel

from kenar.api_client.request import _request


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


class GetUserResponse(BaseModel):
    phone_numbers: List[str]


class GetUserPostsRequest(BaseModel):
    pass


class GetUserPostsResponse(BaseModel):
    class Post(BaseModel):
        token: str
        title: str
        images: List[str] = None
        category: str

    posts: List[Post]


def search_post(data: SearchPostRequest, headers: Dict) -> SearchPostResponse:
    return _request('/v1/open-platform/finder/post', 'POST', data, headers=headers)


def get_post(data: GetPostRequest, headers: Dict):
    return _request(f'/v1/open-platform/finder/post/{data.token}', 'GET', data, headers=headers)


def get_user(data: GetUserRequest, headers: Dict) -> GetUserResponse:
    return GetUserResponse(
        **_request(f'/v1/open-platform/users', 'POST', data, headers=headers).json())


def get_user_posts(data: GetUserPostsRequest, headers: Dict) -> GetUserPostsResponse:
    return GetUserPostsResponse(
        **_request(f'/v1/open-platform/finder/user-posts', 'GET', data, headers=headers).json())
