# pylint: disable=cyclic-import
"""API routes"""
from answers_service import API
from .answers import UserAnswer, GroupAnswers, FormAnswers
API.add_resource(UserAnswer, '/answers/new')
API.add_resource(GroupAnswers, '/answers/group/<form_id>/<group_id>')
API.add_resource(FormAnswers, '/answers/form/<form_id>')
