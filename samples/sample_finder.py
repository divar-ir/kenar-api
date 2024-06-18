from kenar.api_client.finder import GetPostRequest, SearchPostRequest
from samples.sample_bot import bot

if __name__ == '__main__':
    resp = bot.finder.get_post(GetPostRequest(token='wYIw8OJp'))
    print(resp.json())

    resp = bot.finder.search_post(SearchPostRequest(city='tehran', category='light', districts=['abshar', 'nazi-abad'], query={
        'brand_model': {
            'value': ["Pride 111 EX", "MVM 110"]
        },
        'production-year': {
            'min': 1385,
            'max': 1390
        }
    }))
    print(resp.json())

    resp = bot.finder.get_user(data=GetUserRequest(post_token='gZmlPdBK'), access_token='ACCESS_TOKEN_HERE')
    print(resp.json()['phone_numbers'][0])


    resp = bot.finder.get_user_posts(access_token='ACCESS_TOKEN_HERE')
    print(resp.json())

