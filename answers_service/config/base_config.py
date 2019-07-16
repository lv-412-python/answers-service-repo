"""config."""


class Config:
    """Implementation of Configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = '3wffe3423@#Rr23krpo43o4t'
    SQLALCHEMY_DATABASE_URI =\
    'postgres://vcdrrufu:jtbYB9PpKhnEcZ8nQ7nKgEuFCPWvmYZN@balarama.db.elephantsql.com:5432/vcdrrufu'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
