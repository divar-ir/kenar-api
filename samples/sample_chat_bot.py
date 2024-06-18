from kenar.api_client.chatmessage import SendMessageV2Request, BotButton, SetNotifyChatPostConversationsRequest
from kenar.bot import BaseBot
from samples.sample_bot import app_conf

bot = BaseBot(app_conf)

if __name__ == '__main__':
    bot.chat.send_message(
        message_data=SendMessageV2Request(
            user_id='c3c7143f-96f3-4868-9730-0b14e1d6b950',
            peer_id='3d9b0ceb-3556-4a81-bd6e-96ec6028e238',
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

    bot.chat.set_notify_chat_post_conversations(
        data=SetNotifyChatPostConversationsRequest(post_token='gZ6QmeWD', endpoint='https://test2.com',
                                                   identification_key='thest-identification-key'),
        access_token='ACCESS_TOKEN_HERE')
