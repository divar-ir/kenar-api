import os

from kenar.api_client.oauth import OauthResourceType
from kenar.app import Scope, SendChatMessageResourceIdParams, AppOauthConfig
from kenar.errors import APIException
from samples.sample_app import app


oauthConfig = AppOauthConfig(
    oauth_redirect_url=os.environ.get("KENAR_OAUTH_REDIRECT_URL"),
    oauth_secret=os.environ.get('KENAR_OAUTH_SECRET'),
)

if __name__ == '__main__':
    app.add_oauth_service(oauthConfig)
    try:
        state = '348656686'
        scopes = [Scope(resource_type=OauthResourceType.POST_ADDON_CREATE, resource_id='gZ6QmeWD'),
                  Scope(resource_type=OauthResourceType.USER_ADDON_CREATE),
                  Scope(resource_type=OauthResourceType.USER_POSTS_GET),
                  Scope(resource_type=OauthResourceType.USER_PHONE),
                  Scope(resource_type=OauthResourceType.CHAT_MESSAGE_SEND,
                        resource_id=app.oauth.get_send_message_resource_id(
                            SendChatMessageResourceIdParams(user_id='USER_UUID',
                                                            peer_id='PEER_UUID',
                                                            post_token='gZ6QmeWD')),
                        ),
                  ]
        print(app.oauth.get_oauth_redirect(scopes=scopes, state=state))
        code = input('code here')
        print(app.oauth.get_access_token(authorization_token=code))
    except APIException as e:
        print(e)

