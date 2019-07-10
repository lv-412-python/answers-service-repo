""" production config."""
from answers_service.config.base_config import Config


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """production config."""
    DEBUG = False
