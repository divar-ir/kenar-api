from typing import Dict

import httpx
from pydantic import BaseModel

from kenar.api_client.request import _request


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires: int


class OAuthAccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str

    def dict(self, *args, **kwargs) -> Dict:
        object_dict = super().dict(*args, **kwargs)
        object_dict['grant_type'] = 'authorization_code'

        return object_dict


def get_access_token(client: httpx.Client, data: OAuthAccessTokenRequest) -> AccessTokenResponse:
    return _request(client=client, url='https://api.divar.ir/oauth2/token', data=data, method='POST')
