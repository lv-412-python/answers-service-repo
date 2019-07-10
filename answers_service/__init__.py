# pylint: disable=wrong-import-position
"""Init answers service."""
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api

APP = Flask(__name__)

API = Api(APP)
MA = Marshmallow(APP)
from answers_service.views import resources
