""" methods classes """
from flask import request
from flask_api import status
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.serializers.answer_schema import ANSWERS_SCHEMA, ANSWER_SCHEMA


class UserAnswer(Resource):
    """User answers"""

    def post(self):  # pylint: disable=no-self-use
        """creates new answer
        :return json: new answer
        """
        result = []
        for answer in request.get_json():
            try:
                new_answer = ANSWER_SCHEMA.load(answer).data
            except ValidationError as err:
                return err.messages, status.HTTP_400_BAD_REQUEST

            add_new_answer = Answer(
                reply=new_answer['reply'],
                user_id=new_answer['user_id'],
                form_id=new_answer['form_id'],
                field_id=new_answer['field_id'],
                group_id=new_answer['group_id']
            )
            DB.session.add(add_new_answer)
            try:
                DB.session.commit()
                result.append(ANSWER_SCHEMA.dump(new_answer).data)
            except IntegrityError as err:
                DB.session.rollback()
                return {'error': '{} already exist'.format(new_answer)}, status.HTTP_400_BAD_REQUEST
        return result


class GroupAnswers(Resource):
    """gets groups answers"""

    def get(self, form_id, group_id):  # pylint: disable=no-self-use
        """gets groups answers
        :param form_id: int: form id
        :param group_id: int: group_id
        :return json: group answers
        """
        if form_id.isnumeric() and group_id.isnumeric():
            try:
                group_answers = Answer.query.filter_by(form_id=form_id, group_id=group_id)
            except OperationalError:
                return {'error': 'database is not responding'}
            result = ANSWERS_SCHEMA.dump(group_answers).data
        else:
            result = {'message': 'Not correct URL'}
        return result if result else ({"error": "no such row"}, status.HTTP_404_NOT_FOUND)


class FormAnswers(Resource):
    """gets all answers of the form
    :param form_id: int: form
    :return json: form answers"""

    def get(self, form_id):  # pylint: disable=no-self-use
        """get method"""
        if form_id.isnumeric():
            form_answers = Answer.query.filter_by(form_id=form_id)
            result = ANSWERS_SCHEMA.dump(form_answers).data
        else:
            result = {'message': 'Not correct URL'}, status.HTTP_400_BAD_REQUEST
        return result if result else ({"error": "no such row"}, status.HTTP_404_NOT_FOUND)
