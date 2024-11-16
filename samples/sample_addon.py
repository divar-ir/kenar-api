from kenar import (
    CreatePostAddonRequest,
    GetUserAddonsRequest,
    DeleteUserAddonRequest,
    GetPostAddonsRequest,
    DeletePostAddonRequest,
    CreateUserAddonRequest,
    IconName,
    Icon,
    TitleRow,
    SubtitleRow,
    SelectorRow,
    ScoreRow,
    GroupInfo,
    EventRow,
    EvaluationRow,
    DescriptionRow,
    Color,
    WideButtonBar,
)

from samples.sample_app import app

ACCESS_TOKEN = ""
LINK = ""
PHONE = ""
POST_TOKEN = ""


if __name__ == "__main__":
    rsp = app.addon.upload_image("PATH_TO_FILE")
    print(rsp.image_name)
    image_name = rsp.image_name

    # create widgets for addon
    title_row = TitleRow(
        text="این یک نمونه تایتل میباشد", text_color=Color.COLOR_UNSPECIFIED
    )

    subtitle_row = SubtitleRow(text="این یک سابتایتل میباشد")

    desc_row = DescriptionRow(
        text="سلام - این یک ویجت تستی میباشد.",
        has_divider=True,
        is_primary=True,
        expandable=False,
        padded=True,
    )

    eval_row = EvaluationRow(
        indicator_text="متن اندیکاتور",
        indicator_percentage=50,
        indicator_icon=Icon(icon_name=IconName.DOWNLOAD),
        indicator_color=Color.SUCCESS_PRIMARY,
        left=EvaluationRow.Section(
            text="سمت چپ",
            text_color=Color.COLOR_UNSPECIFIED,
            section_color=Color.SUCCESS_PRIMARY,
        ),
        middle=EvaluationRow.Section(
            text="وسط",
            text_color=Color.COLOR_UNSPECIFIED,
            section_color=Color.WARNING_PRIMARY,
        ),
        right=EvaluationRow.Section(
            text="سمت راستی",
            text_color=Color.COLOR_UNSPECIFIED,
            section_color=Color.COLOR_UNSPECIFIED,
        ),
    )

    event_row = EventRow(
        title="تایتل",
        subtitle="سابتایتل",
        has_indicator=False,
        image_url=image_name,
        label="لیبل",
        has_divider=True,
        link=LINK,
        padded=True,
        icon=Icon(icon_name=IconName.ADD),
    )

    group_info = GroupInfo(
        has_divider=True,
        items=[
            GroupInfo.GroupInfoItem(title="تایتل ۱", value="مقدار ۱"),
            GroupInfo.GroupInfoItem(title="تایتل ۲", value="مقدار ۲"),
            GroupInfo.GroupInfoItem(title="تایتل ۳", value="مقدار ۳"),
        ],
    )

    score_row_1 = ScoreRow(
        title="مدل امتیاز کیفی",
        descriptive_score="بسیار عالی",
        score_color=Color.COLOR_UNSPECIFIED,
        link="",
        has_divider=True,
        icon=Icon(icon_name=IconName.ADD),
    )

    score_row_2 = ScoreRow(
        title="مدل امتیاز درصدی",
        percentage_score=100,
        score_color=Color.COLOR_UNSPECIFIED,
        link="",
        has_divider=True,
        icon=Icon(icon_name=IconName.ADD),
    )

    selector_row = SelectorRow(
        title="این یک ویجت سلکتور میباشد",
        has_divider=True,
        has_arrow=True,
        icon=Icon(icon_name=IconName.INFO),
        link=LINK,
    )

    wide_button_bar = WideButtonBar(
        button=WideButtonBar.Button(
            title="به سمت سایت شما", link=LINK
        ),
    )

    resp = app.addon.create_post_addon(
        access_token=ACCESS_TOKEN,
        data=CreatePostAddonRequest(
            token=POST_TOKEN,
            widgets=[
                title_row,
                subtitle_row,
                desc_row,
                eval_row,
                event_row,
                group_info,
                selector_row,
                wide_button_bar,
            ],
        ),
    )
    print(resp)

    resp = app.addon.get_post_addons(data=GetPostAddonsRequest(token=POST_TOKEN))
    print(resp)

    resp = app.addon.delete_post_addon(
        data=DeletePostAddonRequest(token=POST_TOKEN)
    )
    print(resp)

    resp = app.addon.get_post_addons(data=GetPostAddonsRequest(token=POST_TOKEN))
    print(resp)

    resp = app.addon.create_user_addon(
        access_token=ACCESS_TOKEN,
        data=CreateUserAddonRequest(
            phone=PHONE,
            widgets=[desc_row],
            notes="test note",
            categories=[],
        ),
    )
    print(resp)
    user_addon_id = resp.id

    resp = app.addon.get_user_addons(data=GetUserAddonsRequest(phone=PHONE))
    print(resp)

    resp = app.addon.delete_user_addon(data=DeleteUserAddonRequest(id=user_addon_id))
    print(resp)

    resp = app.addon.get_user_addons(data=GetUserAddonsRequest(phone=PHONE))
    print(resp)
