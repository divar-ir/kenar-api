import logging
import os

from dotenv import load_dotenv

from kenar.app import AppConfig, KenarApp

load_dotenv()

logging.basicConfig(level=logging.INFO)

app_conf = AppConfig(app_slug=os.environ.get("KENAR_APP_SLUG"),
                     api_key=os.environ.get("KENAR_API_KEY"),)

app = KenarApp(app_conf)
