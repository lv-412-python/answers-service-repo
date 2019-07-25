"""DB configuration."""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from answers_service import APP

DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)
