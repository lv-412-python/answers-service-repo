""" methods classes """
from sqlalchemy.exc import OperationalError, DataError
from flask import request, jsonify
from flask_restful import Resource
from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.serializers.answer_schema import ANSWERS_SCHEMA, ANSWER_SCHEMA

class UserAnswer(Resource):
    """User answers"""

    def post(self):  # pylint: disable=no-self-use
        """creates new answer
        :return json: new answer
        """
        req_data = request.get_json()
        result = []
        for answer in req_data:
            reply = answer['reply']
            user_id = answer['user_id']
            form_id = answer['form_id']
            field_id = answer['field_id']
            group_id = answer['group_id']
            try:
                exists = Answer.query.filter_by(user_id=user_id, form_id=form_id,
                                                field_id=field_id).first()
            except DataError:
                return jsonify({'error': "input data not valid"}), 400

            if exists:
                result = ({'error': 'this answer alreasy exist'}, 203)
                break
            else:
                new_answer = Answer(reply=reply, user_id=user_id, form_id=form_id,
                                    field_id=field_id, group_id=group_id)
                DB.session.add(new_answer)  # pylint: disable=no-member
                try:
                    DB.session.commit()  # pylint: disable=no-member
                    result.append(ANSWER_SCHEMA.dump(new_answer).data)
                except OperationalError:
                    result = {'error': 'database is not responding'}, 400
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
        return result if result else ({"error": "no such row"}, 404)


class FormAnswers(Resource):
    """gets all answers of the form
    :param form_id: int: form
    :return json: form answers"""

    def get(self, form_id):  # pylint: disable=no-self-use
        """get method"""
        if form_id.isnumeric():
            try:
                form_answers = Answer.query.filter_by(form_id=form_id)
            except OperationalError:
                return {'error': 'database is not responding'}, 400
            result = ANSWERS_SCHEMA.dump(form_answers).data
        else:
            result = {'message': 'Not correct URL'}, 400
        return result if result else ({"error": "no such row"}, 404)
