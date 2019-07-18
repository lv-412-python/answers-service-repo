# pylint: disable=wrong-import-position
"""Init answers service."""
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)
API = Api(APP)
MA = Marshmallow(APP)
from answers_service.views import resources
