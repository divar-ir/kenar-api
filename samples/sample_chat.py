from kenar.models.chatmessage import SendMessageV2Request, BotButton, SetNotifyChatPostConversationsRequest
from samples.sample_app import app

if __name__ == '__main__':
    app.chat.send_message(
        data=SendMessageV2Request(
            user_id='USER_UUID',
            peer_id='PEER_UUID',
            post_token='gZ6QmeWD',
            type='TEXT',
            message='سلام این پیام تستی است',
            sender_btn=BotButton(
                data=BotButton.ButtonData(icon_name='SEND', caption='direct link', direct_link='https://divar.ir'),
                action=BotButton.Action.DIRECT_LINK),
            receiver_btn=BotButton(
                data=BotButton.ButtonData(icon_name='DELETE', caption='dynamic link', direct_link='https://divar2.ir'),
                action=BotButton.Action.LINK)

        ),
        access_token='ACCESS_TOKEN_HERE')

    app.chat.set_notify_chat_post_conversations(
        data=SetNotifyChatPostConversationsRequest(post_token='gZ6QmeWD', endpoint='https://test2.com',
                                                   identification_key='thest-identification-key'),
        access_token='ACCESS_TOKEN_HERE')
