import os

import httpx

from kenar.models.chatmessage import SetNotifyChatPostConversationsRequest
from kenar.models.oauth import OauthResourceType
from kenar.app import Scope, SendChatMessageResourceIdParams
from samples.sample_app import app


post_token = "gZ2J5i8M"
user_id = "e912b6f5-fba1-4cb9-b862-d7b166a89cf0"
peer_id = "d3ca860d-aa3b-4e47-9ed0-2e4c54b96663"
APP_ENDPOINT = "https://divar-kenar-example.darkube.app/chat/receive_notify"



if __name__ == '__main__':
    try:
        state = '348656686'
        scopes = [
            Scope(resource_type=OauthResourceType.CHAT_MESSAGE_SEND,
                resource_id=app.oauth.get_send_message_resource_id(
                    SendChatMessageResourceIdParams(user_id=user_id,
                                                    peer_id=peer_id,
                                                    post_token=post_token))),
            Scope(resource_type=OauthResourceType.CHAT_POST_CONVERSATIONS_READ, resource_id=post_token)
        ]
        print(app.oauth.get_oauth_redirect(scopes=scopes, state=state))
        code = input('code here')
        access_token_response = app.oauth.get_access_token(authorization_token=code)
        print(access_token_response)
        # app.chat.set_notify_chat_post_conversations(access_token=access_token_response.access_token,
        #                                             data=SetNotifyChatPostConversationsRequest(
        #                                             post_token=post_token,
        #                                             endpoint=APP_ENDPOINT,
        #                                             identification_key="nemidoonam",
        #                                               ))
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        print(e)

