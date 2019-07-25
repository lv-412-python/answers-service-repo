"""Init answers service.""" # pylint: disable=wrong-import-position
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_cors import CORS
from answers_service.config.prod_config import ProductionConfig

APP = Flask(__name__)
CORS(APP)
API = Api(APP)
MA = Marshmallow(APP)

APP.config.from_object(ProductionConfig)

from answers_service.views import resources
