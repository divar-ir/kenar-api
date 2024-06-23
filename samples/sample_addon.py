from kenar.models.addon import CreatePostAddonRequest, Widgets, Widget, CreateUserAddonRequest, \
    GetPostAddonsRequest, DeletePostAddonRequest, GetUserAddonsRequest, DeleteUserAddonRequest
from samples.sample_app import app

if __name__ == '__main__':
    resp = app.addon.create_post_addon(
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
                    "fallback_link": "https://test.path.com",
                    "payload": {
                        "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                        "url": "https://test.path.com"
                    }
                }
            })]),
        ),
    )
    print(resp)
    resp = app.addon.get_post_addons(data=GetPostAddonsRequest(token='gZW5uQcs'))
    print(resp)

    resp = app.addon.delete_post_addon(data=DeletePostAddonRequest(token='gZW5uQcs'))
    print(resp)

    resp = app.addon.get_post_addons(data=GetPostAddonsRequest(token='gZW5uQcs'))
    print(resp)

    resp = app.addon.create_user_addon(
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
                    "fallback_link": "https://test.path.com",
                    "payload": {
                        "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                        "url": "https://test.path.com"
                    }
                }
            })]),
            notes='test note',
            categories=[]
        ),
    )
    print(resp)
    user_addon_id = resp.id

    resp = app.addon.get_user_addons(data=GetUserAddonsRequest(phone='PHONE_NUMBER'))
    print(resp)

    resp = app.addon.delete_user_addon(data=DeleteUserAddonRequest(id=user_addon_id))
    print(resp)

    resp = app.addon.get_user_addons(data=GetUserAddonsRequest(phone='PHONE_NUMBER'))
    print(resp)
