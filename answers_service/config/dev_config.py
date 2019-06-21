""" development config """
from answers_service.config.base_config import Config


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """ development config """
    DEVELOPMENT = True
    DEBUG = True
