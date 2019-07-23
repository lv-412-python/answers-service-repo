"""config."""


class Config:
    """Implementation of Configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = '3wffe3423@#Rr23krpo43o4t'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:mysecretpassword@db:5432/4m_answers'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
