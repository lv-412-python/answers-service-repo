""" methods classes """
from flask import request
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
            exists = bool(Answer.query.filter_by(user_id=user_id, form_id=form_id,
                                                 field_id=field_id).first())
            if exists:
                result = ({'error': 'this answer alreasy exist'}, 203)
                break
            else:
                new_answer = Answer(reply=reply, user_id=user_id, form_id=form_id,
                                    field_id=field_id, group_id=group_id)
                DB.session.add(new_answer)  # pylint: disable=no-member
                DB.session.commit()  # pylint: disable=no-member
                result.append(ANSWER_SCHEMA.dump(new_answer).data)
        return result


class GroupAnswers(Resource):
    """gets groups answers"""

    def get(self, form_id, group_id):  # pylint: disable=no-self-use
        """gets groups answers
        :param form_id: int: form id
        :param group_id: int: group_id
        :return json: group answers
        """
        group_answers = Answer.query.filter_by(form_id=form_id, group_id=group_id)
        result = ANSWERS_SCHEMA.dump(group_answers).data
        return result if result != [] else {"error": "no such row"}


class FormAnswers(Resource):
    """gets all answers of the form
    :param form_id: int: form
    :return json: form answers"""

    def get(self, form_id):  # pylint: disable=no-self-use
        """get method"""
        form_answers = Answer.query.filter_by(form_id=form_id)
        result = ANSWERS_SCHEMA.dump(form_answers).data
        return result if result != [] else {"error": "no such row"}
