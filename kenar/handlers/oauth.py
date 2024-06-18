import abc
from enum import Enum
from typing import List

from pydantic import BaseModel

from kenar.bot import AccessTokenResponse, Scope
from kenar.handlers.handler import Handler

class AuthorizePayload(BaseModel):
    scopes: List[Scope]
    session_id: str
    state: str


class SessionOauth(BaseModel):
    session_id: str
    scopes: List[Scope]


class AccessTokenPayload(BaseModel):
    authorization_token: str
    session_id: str
    state: str


class OAuthStep(Enum):
    AUTHORIZE = 1
    ACCESS_TOKEN = 2


class OAuth:
    step: OAuthStep


class OauthHandler(Handler):
    def handle(self, oauth: OAuth):
        ...

    def get_oauth_redirect_url(self, payload: AuthorizePayload) -> str:  # redirect to returned url from this function
        self.set_session_oauth_details(payload)
        return self.bot.oauth.get_oauth_redirect(payload.scopes, payload.state)

    def get_access_token(self, payload: AccessTokenPayload) -> AccessTokenResponse:
        self.get_session_oauth_details(session_id=payload.session_id, state=payload.state)
        return self.bot.oauth.get_access_token(payload.authorization_token)

    @abc.abstractmethod
    def get_oauth_random_state(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def set_session_oauth_details(self, payload: AuthorizePayload):
        raise NotImplemented

    @abc.abstractmethod
    def get_session_oauth_details(self, session_id: str, state: str) -> AuthorizePayload:
        raise NotImplemented
