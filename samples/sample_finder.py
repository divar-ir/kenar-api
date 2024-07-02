from kenar import (
    SearchPostRequest,
    GetUserRequest,
    GetUserPostsRequest,
    GetPostRequest,
)
from samples.sample_app import app

if __name__ == "__main__":
    resp = app.finder.get_post(GetPostRequest(token="wYIw8OJp"))
    print(resp)

    resp = app.finder.search_post(
        SearchPostRequest(
            city="tehran",
            category="light",
            districts=["abshar", "nazi-abad"],
            query={
                "brand_model": {"value": ["Pride 111 EX", "MVM 110"]},
                "production-year": {"min": 1385, "max": 1390},
            },
        )
    )
    print(resp)

    resp = app.finder.get_user(data=GetUserRequest(), access_token="ACCESS_TOKEN_HERE")
    print(resp)

    resp = app.finder.get_user_posts(
        data=GetUserPostsRequest(), access_token="ACCESS_TOKEN_HERE"
    )
    print(resp)
