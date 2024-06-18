from kenar.api_client.addon import CreatePostAddonRequest, Widgets, Widget, CreateUserAddonRequest, \
    GetPostAddonsRequest, DeletePostAddonRequest, GetUserAddonsRequest, DeleteUserAddonRequest
from samples.sample_bot import bot

if __name__ == '__main__':
    resp = bot.addon.create_post_addon(
        access_token='ACCESS_TOKEN_HERE',
        data=CreatePostAddonRequest(
            token='gZW5uQcs',
            widgets=Widgets(widget_list=[Widget(widget_type='SCORE_ROW', data={
                "@type": "type.googleapis.com/widgets.ScoreRowData",
                "title": "فنی",
                "percentage_score": 80,
                "score_color": "SUCCESS_PRIMARY",
                "hasDivider": True,
                "icon": {
                    "icon_name": "HISTORY",
                    "icon_color": "SUCCESS_PRIMARY"
                },
                "action": {
                    "type": "LOAD_WEB_VIEW_PAGE",
                    "fallback_link": "https://verification-addon.divar.ir",
                    "payload": {
                        "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                        "url": "https://verification-addon.divar.ir"
                    }
                }
            })]),
        ),
    )
    print(resp.json())

    resp = bot.addon.delete_post_addon(data=DeletePostAddonRequest(token='gZW5uQcs'))
    print(resp.json())

    resp = bot.addon.get_post_addons(data=GetPostAddonsRequest(token='gZW5uQcs'))
    print(resp.json())

    resp = bot.addon.create_user_addon(
        access_token='ACCESS_TOKEN_HERE',
        data=CreateUserAddonRequest(
            phone='09035718581',
            widgets=Widgets(widget_list=[Widget(widget_type='SCORE_ROW', data={
                "@type": "type.googleapis.com/widgets.ScoreRowData",
                "title": "تست",
                "percentage_score": 80,
                "score_color": "SUCCESS_PRIMARY",
                "hasDivider": True,
                "icon": {
                    "icon_name": "HISTORY",
                    "icon_color": "SUCCESS_PRIMARY"
                },
                "action": {
                    "type": "LOAD_WEB_VIEW_PAGE",
                    "fallback_link": "https://verification-addon.divar.ir",
                    "payload": {
                        "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                        "url": "https://verification-addon.divar.ir"
                    }
                }
            })]),
            notes='test note',
            categories=[]
        ),
    )
    print(resp.json())
    user_addon_id = resp.json()['id']

    resp = bot.addon.get_user_addons(data=GetUserAddonsRequest(phone='09035718581'))
    print(resp.json())

    resp = bot.addon.delete_user_addon(data=DeleteUserAddonRequest(id=user_addon_id))
    print(resp.json())

    resp = bot.addon.get_user_addons(data=GetUserAddonsRequest(phone='09035718581'))
    print(resp.json())
