from kenar.bot import Scope
from samples.sample_bot import bot

if __name__ == '__main__':
    state = 'random-state'
    scopes = [
        Scope(scope='USER_PHONE'), Scope(scope='CHAT_POST_CONVERSATIONS_READ', resource_id='gZ6QmeWD')]

    bot.oauth.get_oauth_redirect(scopes=scopes, state=state)

    auth_url = bot.oauth.get_access_token('')

    print(f'click here {auth_url}')
    code = input('please enter authorization token there')
    access_token = oauth_handler.get_access_token(
        AccessTokenPayload(authorization_token=code, session_id=session_id, state=state))
    print(access_token)

    chat_handler.register_notify_on_post_conversations(
        notification=PostConversationsNotificationRegisterPayload(post_token='', phone='',
                                                                  endpoint='https://www.test.com')
    )
    print('registered successfully')

