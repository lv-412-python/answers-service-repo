"""config"""


class Config:  # pylint: disable=too-few-public-methods
    """
        Implementation of Configuration class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = '3wffe3423@#Rr23krpo43o4t'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_answers'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FIELD_SERVICE_URL = 'http://127.0.0.1:5053/api/v1/field'
