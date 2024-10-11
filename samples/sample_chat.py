from kenar import (
    SendMessageRequest,
    BotButton,
)
from samples.sample_app import app

if __name__ == "__main__":
    app.chat.send_message(
        data=SendMessageRequest(
            user_id="USER_UUID",
            peer_id="PEER_UUID",
            post_token="gZ6QmeWD",
            message="سلام این پیام تستی است",
            sender_btn=BotButton(
                caption="direct link",
                direct_link="https://divar.ir",
            ),
            receiver_btn=BotButton(
                caption="dynamic link",
                direct_link="https://divar2.ir",
                extra_data={"key": "value"},
            ),
        ),
        access_token="ACCESS_TOKEN_HERE",
    )
