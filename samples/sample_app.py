import logging
import os

from kenar import ClientConfig, Client

logging.basicConfig(level=logging.INFO)

client_conf = ClientConfig(
    app_slug=os.environ.get("KENAR_APP_SLUG"),
    api_key=os.environ.get("KENAR_API_KEY"),
    oauth_secret=os.environ.get("KENAR_OAUTH_SECRET"),
    oauth_redirect_url=os.environ.get("KENAR_OAUTH_REDIRECT_URL"),
)

app = Client(client_conf)
