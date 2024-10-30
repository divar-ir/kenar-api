import base64
import urllib.parse
from importlib.metadata import version
from typing import List, Optional, Literal, Tuple

import httpx
from pydantic import BaseModel

from kenar.addon import (
    CreateUserAddonRequest,
    CreatePostAddonRequest,
    PostAddon, UserAddon,
)
from kenar.asset import (
    GetCategoriesResponse,
    GetCitiesResponse,
    GetDistrictsResponse,
    GetBrandModelsResponse,
    GetMobileInternalStoragesResponse,
    GetMobileRamMemoriesResponse,
    GetLightBodyStatusResponse,
    GetColorsResponse,
)
from kenar.chatmessage import (
    SendMessageRequest,
)
from kenar.finder import (
    SearchPostRequest,
    SearchPostResponse,
    GetPostRequest,
    GetUserRequest,
    GetUserPostsRequest,
    GetUserResponse,
    GetUserPostsResponse,
    GetPostResponse,
)
from kenar.oauth import OAuthAccessTokenRequest, AccessTokenResponse
from kenar.oauth import Scope, SendChatMessageResourceIdParams
from kenar.request import retry

ACCESS_TOKEN_HEADER_NAME = "x-access-token"


class ClientConfig(BaseModel):
    app_slug: str
    api_key: str
    oauth_secret: str
    oauth_redirect_url: str


class ChatService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def send_message(
            self,
            access_token: str,
            data: SendMessageRequest,
            max_retry=3,
            retry_delay=1,
    ) -> Tuple[int, str]:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url="/v2/open-platform/chat/conversation",
                data=data.as_dict(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token},
            )

        rsp = send_request()
        rsp_json = rsp.json()

        status, message = rsp_json.get("status", 0), rsp_json.get("message", "")
        return status, message


class FinderService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def search_post(
            self,
            data: SearchPostRequest,
            max_retry=3,
            retry_delay=1,
    ) -> SearchPostResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url="/v1/open-platform/finder/post", content=data.json()
            )

        rsp = send_request()
        return SearchPostResponse(**rsp.json())

    def get_post(
            self,
            data: GetPostRequest,
            max_retry=3,
            retry_delay=1,
    ) -> GetPostResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url=f"/v1/open-platform/finder/post/{data.token}",
                content=data.json(),
            )

        rsp = send_request()
        return GetPostResponse(**rsp.json())

    def get_user(
            self,
            access_token: str,
            data: GetUserRequest = None,
            max_retry=3,
            retry_delay=1,
    ):
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url="/v1/open-platform/users",
                content=data.json() if data is not None else "",
                headers={ACCESS_TOKEN_HEADER_NAME: access_token},
            )

        rsp = send_request()
        return GetUserResponse(**rsp.json())

    def get_user_posts(
            self,
            access_token: str,
            data: Optional[GetUserPostsRequest] = None,
            max_retry=3,
            retry_delay=1,
    ):
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.get(
                url="/v1/open-platform/finder/user-posts",
                params=data.json() if data is not None else "",
                headers={ACCESS_TOKEN_HEADER_NAME: access_token},
            )

        rsp = send_request()
        return GetUserPostsResponse(**rsp.json())


class AddonService:
    def __init__(self, client: httpx.Client):
        self._client = client

    def create_user_addon(
            self,
            access_token: str,
            data: CreateUserAddonRequest,
            max_retry=3,
            retry_delay=1,
    ) -> str:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url=f"/v1/open-platform/addons/user/{data.phone}",
                data=data.to_dict(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token},
            )

        rsp = send_request()
        addon_id = rsp.json().get("id", "")
        return addon_id

    def delete_user_addon(
            self,
            addon_id: str,
            max_retry=3,
            retry_delay=1,
    ):
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.delete(url=f"/v1/open-platform/addons/user/{addon_id}")

        send_request()

    def get_user_addons(
            self,
            phone: str,
            max_retry=3,
            retry_delay=1,
    ) -> List[UserAddon]:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.get(url=f"/v1/open-platform/addons/user/{phone}")

        rsp = send_request()
        addons = rsp.json().get("addons", [])
        return [UserAddon(**addon) for addon in addons]

    def create_post_addon(
            self,
            access_token: str,
            data: CreatePostAddonRequest,
            max_retry=3,
            retry_delay=1,
    ):
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url=f"/v1/open-platform/addons/post/{data.token}",
                data=data.to_dict(),
                headers={ACCESS_TOKEN_HEADER_NAME: access_token},
            )

        send_request()

    def delete_post_addon(self, token: str, max_retry=3, retry_delay=1):
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.delete(url=f"/v1/open-platform/addons/post/{token}")

        send_request()

    def upload_image(
            self,
            path: str,
            max_retry=3,
            retry_delay=1,
    ) -> str:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            with open(path, "rb") as f:
                file_content = f.read()
            return self._client.put(
                url="https://divar.ir/v2/image-service/open-platform/image.jpg",
                content=file_content,
                headers={"Content-Type": "image/jpeg"},
            )

        rsp = send_request()
        image_name = rsp.json().get("image_name", "")
        return image_name

    def get_post_addons(
            self,
            token: str,
            max_retry=3,
            retry_delay=1,
    ) -> List[PostAddon]:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.get(url=f"/v1/open-platform/addons/post/{token}")

        rsp = send_request()
        addons = rsp.json().get("addons", [])
        return [PostAddon(**addon) for addon in addons]


class AssetService:
    def __init__(self, client):
        self._client = client

    def get_categories(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetCategoriesResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/category",
            )

        rsp = send_request()
        return GetCategoriesResponse(**rsp.json())

    def get_cities(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetCitiesResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/city",
            )

        rsp = send_request()
        return GetCitiesResponse(**rsp.json())

    def get_districts(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetDistrictsResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/district",
            )

        rsp = send_request()
        return GetDistrictsResponse(**rsp.json())

    def get_city_districts(
            self,
            city: str,
            max_retry=3,
            retry_delay=1,
    ) -> GetDistrictsResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url=f"https://api.divar.ir/v1/open-platform/assets/district/{city}",
            )

        rsp = send_request()
        return GetDistrictsResponse(**rsp.json())

    def get_brand_models(
            self,
            category: Literal["light", "mobile-phones"],
            max_retry=3,
            retry_delay=1,
    ) -> GetBrandModelsResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url=f"https://api.divar.ir/v1/open-platform/assets/brand-model/{category}",
            )

        rsp = send_request()
        return GetBrandModelsResponse(**rsp.json())

    def get_colors(
            self,
            category: Literal["light", "mobile-phones"],
            max_retry=3,
            retry_delay=1,
    ) -> GetColorsResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url=f"https://api.divar.ir/v1/open-platform/assets/color/{category}",
            )

        rsp = send_request()
        return GetColorsResponse(**rsp.json())

    def get_mobile_internal_storages(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetMobileInternalStoragesResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/internal-storage",
            )

        rsp = send_request()
        return GetMobileInternalStoragesResponse(**rsp.json())

    def get_mobile_ram_memories(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetMobileRamMemoriesResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/ram-memory",
            )

        rsp = send_request()
        return GetMobileRamMemoriesResponse(**rsp.json())

    def get_light_body_status(
            self,
            max_retry=3,
            retry_delay=1,
    ) -> GetLightBodyStatusResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.request(
                method="GET",
                url="https://api.divar.ir/v1/open-platform/assets/body-status",
            )

        rsp = send_request()
        return GetLightBodyStatusResponse(**rsp.json())


class OAuthService:
    def __init__(self, client, app_slug, oauth_redirect_url, oauth_secret):
        self._app_slug = app_slug
        self._oauth_redirect_url = oauth_redirect_url
        self._oauth_secret = oauth_secret
        self._client = client

    def get_oauth_redirect(self, scopes: List[Scope], state: str) -> str:
        scope = [
            (
                f"{scope.resource_type.value}.{scope.resource_id}"
                if scope.resource_id is not None
                else scope.resource_type
            )
            for scope in scopes
        ]
        return (
            f"https://api.divar.ir/oauth2/auth?"
            f"response_type=code&"
            f"client_id={urllib.parse.quote(self._app_slug)}&"
            f"state={state}&"
            f"redirect_uri={urllib.parse.quote(self._oauth_redirect_url)}&"
            f"scope={urllib.parse.quote_plus(" ".join(scope))}"
        )

    def get_access_token(
            self,
            authorization_token: str,
            max_retry=3,
            retry_delay=1,
    ) -> AccessTokenResponse:
        @retry(max_retries=max_retry, delay=retry_delay)
        def send_request():
            return self._client.post(
                url="/oauth2/token",
                data=OAuthAccessTokenRequest(
                    client_id=self._app_slug,
                    client_secret=self._oauth_secret,
                    code=authorization_token,
                    redirect_uri=self._oauth_redirect_url,
                ).as_dict(),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        rsp = send_request()
        return AccessTokenResponse(**rsp.json())

    @staticmethod
    def get_send_message_resource_id(params: SendChatMessageResourceIdParams) -> str:
        return base64.b64encode(
            f"{params.user_id}:{params.post_token}:{params.peer_id}".encode("utf-8")
        ).decode("utf-8")


class Client:
    def __init__(self, conf: ClientConfig):
        if not conf.api_key:
            raise ValueError("the KENAR_API_KEY environment variable must be set")
        if not conf.app_slug:
            raise ValueError("the KENAR_APP_SLUG environment variable must be set")
        if not conf.oauth_redirect_url:
            raise ValueError(
                "the KENAR_OAUTH_REDIRECT_URL environment variable must be set"
            )
        if not conf.oauth_secret:
            raise ValueError("the KENAR_OAUTH_SECRET environment variable must be set")

        self.app_config = conf

        self._client = httpx.Client(
            timeout=1,
            headers={
                "KenarDivarSDK-Version": version("Kenar"),
                "x-api-key": conf.api_key,
                "Content-Type": "application/json",
            },
            base_url="https://api.divar.ir",
        )
        self._oauth = OAuthService(
            client=self._client,
            app_slug=self.app_config.app_slug,
            oauth_redirect_url=conf.oauth_redirect_url,
            oauth_secret=conf.oauth_secret,
        )
        self._finder = FinderService(self._client)
        self._chat = ChatService(self._client)
        self._addon = AddonService(self._client)
        self._asset = AssetService(self._client)

    @property
    def chat(self):
        return self._chat

    @chat.setter
    def chat(self, service: ChatService):
        if not isinstance(service, ChatService):
            raise ValueError("chat must be an instance of ChatService")
        self._chat = service

    @property
    def finder(self):
        return self._finder

    @finder.setter
    def finder(self, service: FinderService):
        if not isinstance(service, FinderService):
            raise ValueError("finder must be an instance of FinderService")
        self._finder = service

    @property
    def addon(self):
        return self._addon

    @addon.setter
    def addon(self, service: AddonService):
        if not isinstance(service, AddonService):
            raise ValueError("addon must be an instance of AddonService")
        self._addon = service

    @property
    def oauth(self):
        return self._oauth

    @oauth.setter
    def oauth(self, service: OAuthService):
        if not isinstance(service, OAuthService):
            raise ValueError("addon must be an instance of OAuthService")
        self._oauth = service

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, service: AssetService):
        if not isinstance(service, AssetService):
            raise ValueError("addon must be an instance of AssetService")
        self._asset = service
