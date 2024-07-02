import httpx

from kenar import OauthResourceType, Scope, SendChatMessageResourceIdParams
from samples.sample_app import app


if __name__ == "__main__":
    try:
        state = "348656686"
        scopes = [
            Scope(
                resource_type=OauthResourceType.POST_ADDON_CREATE,
                resource_id="POST_TOKEN_HERE",
            ),
            Scope(resource_type=OauthResourceType.USER_ADDON_CREATE),
            Scope(resource_type=OauthResourceType.USER_POSTS_GET),
            Scope(resource_type=OauthResourceType.USER_PHONE),
            Scope(
                resource_type=OauthResourceType.CHAT_MESSAGE_SEND,
                resource_id=app.oauth.get_send_message_resource_id(
                    SendChatMessageResourceIdParams(
                        user_id="USER_UUID",
                        peer_id="PEER_UUID",
                        post_token="POST_TOKEN_HERE",
                    )
                ),
            ),
        ]
        print(app.oauth.get_oauth_redirect(scopes=scopes, state=state))
        code = input("code here")
        print(app.oauth.get_access_token(authorization_token=code))
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        print(e)
