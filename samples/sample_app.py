import logging
import os

from dotenv import load_dotenv

from kenar.app import AppConfig, KenarApp

load_dotenv()

logging.basicConfig(level=logging.INFO)

app_conf = AppConfig(app_slug=os.environ.get("KENAR_APP_SLUG"),
                     api_key=os.environ.get("KENAR_API_KEY"),
                     oauth_secret=os.environ.get("KENAR_OAUTH_SECRET"),
                     oauth_redirect_url=os.environ.get("KENAR_OAUTH_REDIRECT_URL"),
                     )

app = KenarApp(app_conf)
