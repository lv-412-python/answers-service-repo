""" methods classes """
import requests
from flask import request
from flask_restful import Resource

from answers_service.config.base_config import Config
from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.serializers.answer_schema import ANSWERS_SCHEMA, ANSWER_SCHEMA


def get_field_title_by_id(result):
    """changes field_id to field_title
    :param result: list: result of sqlalchemy query
    :return dict
    """
    # creates set of fields_id
    fields_id = set()
    for i, _ in enumerate(result):
        field = result[i]["field_id"]
        fields_id.add(int(field))
    # request titles based on needed fields_id
    fields_json = {'fields': list(fields_id)}
    fields_request = requests.get(Config.FIELD_SERVICE_URL, json=fields_json)
    r_dict = fields_request.json()
    # delete field_id and add field_title
    for i, _ in enumerate(result):
        field = result[i]["field_id"]
        result[i]["field_title"] = r_dict[str(field)]
    return result


class UserAnswer(Resource):
    """User answers"""

    def post(self):  # pylint: disable=no-self-use
        """creates new answer
        :return json: new answer
        """
        reply = request.json['reply']
        user_id = request.json['user_id']
        form_id = request.json['form_id']
        field_id = request.json['field_id']
        group_id = request.json['group_id']

        # check if such answer exists
        exists = bool(Answer.query.filter_by(user_id=user_id, form_id=form_id,
                                             group_id=group_id, field_id=field_id).first())
        if exists:
            result = ({'error': 'this answer alreasy exist'}, 203)
        else:
            new_answer = Answer(reply=reply, user_id=user_id, form_id=form_id,
                                field_id=field_id, group_id=group_id)
            DB.session.add(new_answer)  # pylint: disable=no-member
            DB.session.commit()  # pylint: disable=no-member
            result = ANSWER_SCHEMA.jsonify(new_answer)
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
        response = get_field_title_by_id(result)
        return response if response != [] else {"error": "no such row"}


class FormAnswers(Resource):
    """gets all answers of the form
    :param form_id: int: form
    :return json: form answers"""

    def get(self, form_id):  # pylint: disable=no-self-use
        """get method"""
        form_answers = Answer.query.filter_by(form_id=form_id)
        result = ANSWERS_SCHEMA.dump(form_answers).data
        response = get_field_title_by_id(result)
        return response if response != [] else {"error": "no such row"}
