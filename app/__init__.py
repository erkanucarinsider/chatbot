import certifi
import ssl

from os import environ

from flask import Flask
from dotenv import load_dotenv
from slack_bolt import App
from slack_sdk import WebClient
from slack_bolt.adapter.flask import SlackRequestHandler

from config import config as app_config

APPLICATION_ENV = environ.get('ENV', 'development')


def create_app():
    load_dotenv()
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    ssl._create_default_https_context = ssl._create_unverified_context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    token = app_config[APPLICATION_ENV].SLACK_BOT_TOKEN
    signing_secret = app_config[APPLICATION_ENV].SLACK_SIGNING_SECRET
    slack_client = WebClient(token=token, ssl=ssl_context)
    slack_app = App(client=slack_client, signing_secret=signing_secret)
    handler = SlackRequestHandler(slack_app)

    return app, slack_app, handler
