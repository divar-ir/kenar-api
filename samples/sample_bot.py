import logging
import os

from dotenv import load_dotenv

from kenar.bot import AppConfig, BaseBot

load_dotenv()

logging.basicConfig(level=logging.INFO)

app_conf = AppConfig(app_slug=os.environ.get("KENAR_APP_SLUG"),
                     api_key=os.environ.get("KENAR_API_KEY"),
                     identification_key=os.environ.get("KENAR_IDENT_KEY"),
                     oauth_redirect_url=os.environ.get("KENAR_OAUTH_REDIRECT_URL"),
                     oauth_secret=os.environ.get('KENAR_OAUTH_SECRET'))

bot = BaseBot(app_conf)
