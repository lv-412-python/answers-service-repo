"""Configuration for testing."""
from answers_service.config.base_config import Config


class TestConfiguration(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_answers_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False