# pylint: disable=cyclic-import
"""API routes."""
from answers_service import API
from .answers import UserAnswer

API.add_resource(UserAnswer, '/answers')
