""" production config."""
from answers_service.config.base_config import Config


class ProductionConfig(Config):
    """production config."""
    DEBUG = False
