""" methods classes """
from flask import request
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

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
            add_new_answer = Answer(**new_answer)
            DB.session.add(add_new_answer)
            try:
                DB.session.commit()
                result.append(ANSWER_SCHEMA.dump(new_answer).data)
            except IntegrityError:
                DB.session.rollback()
                return {'error': '{} already exist'.format(new_answer)}, status.HTTP_400_BAD_REQUEST
        return result


    def get(self):  # pylint: disable=no-self-use
        """gets all answers of the form
        :return json: answers"""
        try:
            form_id = request.args['form_id']
        except HTTPException:
            return {'message': 'form_id is not passed'}, status.HTTP_400_BAD_REQUEST
        group_id = request.args.getlist('group_id', type=int)
        from_date = request.args.get('from_date')
        end_date = request.args.get('end_date')
        form_answers = Answer.query.filter(Answer.form_id == form_id)
        if from_date:
            form_answers = form_answers.filter(Answer.answer_date >= from_date)
        if end_date:
            form_answers = form_answers.filter(Answer.answer_date <= end_date)
        if group_id:
            form_answers = form_answers.filter(Answer.group_id.in_(group_id))
        result = ANSWERS_SCHEMA.dump(form_answers).data
        return result if result else ({"error": "no such row"}, status.HTTP_404_NOT_FOUND)
