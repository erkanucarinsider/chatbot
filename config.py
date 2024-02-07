from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base configuration class for all environments"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = environ.get('ENV') or 'development'
    APP_NAME = environ.get('APP_NAME') or 'chatbotexample'
    SLACK_SIGNING_SECRET = environ.get('SLACK_SIGNING_SECRET')
    SLACK_BOT_TOKEN = environ.get('SLACK_BOT_TOKEN')


class Production(Config):
    """Production configuration class"""
    ENV = 'production'


class Development(Config):
    """Development configuration class"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = 'development'


config = {
    'development': Development,
    'production': Production,
}
