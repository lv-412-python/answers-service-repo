"""config."""
LOCAL_DATABASE = 'postgres://postgres:postgres@localhost:5432/4m_answers'
DOCKER_DB = 'postgres://postgres:mysecretpassword@db:5432/4m_answers'

class Config:
    """Implementation of Configuration class."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DOCKER_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = True
