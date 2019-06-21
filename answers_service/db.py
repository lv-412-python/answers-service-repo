""" DB configuration """
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from answers_service.config.dev_config import DevelopmentConfig
from answers_service import APP

APP.config.from_object(DevelopmentConfig)
DB = SQLAlchemy(APP)


MIGRATE = Migrate(APP, DB)
