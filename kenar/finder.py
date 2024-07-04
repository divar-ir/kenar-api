from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel


class SearchPostRequest(BaseModel):
    city: Optional[str]
    districts: Optional[List[str]]
    category: Optional[str]
    query: dict


class SearchPostResponse(BaseModel):
    posts: List[dict] = None


class GetPostRequest(BaseModel):
    token: str


class PostExtState(str, Enum):
    UNKNOWN = "UNKNOWN"
    PUBLISHED = "PUBLISHED"
    REVIEW_REQ = "REVIEW_REQ"
    PAYMENT_REQ = "PAYMENT_REQ"
    RETIRED = "RETIRED"


class GetPostResponse(BaseModel):
    state: PostExtState
    first_published_at: str
    token: str
    category: str
    city: str
    district: str
    data: Dict


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
