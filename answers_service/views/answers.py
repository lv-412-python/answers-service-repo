""" methods classes """
from flask import request
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError, fields
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import parser

from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.serializers.answer_schema import ANSWERS_SCHEMA, ANSWER_SCHEMA


class UserAnswer(Resource):
    """User answers"""

    def post(self):  # pylint: disable=no-self-use
        """creates new answer.
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
        return result, status.HTTP_201_CREATED

    def get(self):  # pylint: disable=no-self-use
        """gets all answers of the form.
        :return json: answers"""
        url_args = {
            'form_id': fields.Int(required=True, validate=lambda val: val > 0),
            'group_id': fields.List(fields.Int(validate=lambda val: val > 0)),
            'from_date': fields.Date(),
            'end_date': fields.Date()
        }
        try:
            args = parser.parse(url_args, request)
        except HTTPException:
            return {"error": "not correct URL"}, status.HTTP_400_BAD_REQUEST
        form_answers = Answer.query.filter(Answer.form_id == args['form_id'])
        if 'from_date' in args:
            form_answers = form_answers.filter(Answer.answer_date >= args['from_date'])
        if 'end_date' in args:
            form_answers = form_answers.filter(Answer.answer_date <= args['end_date'])
        if 'group_id' in args:
            form_answers = form_answers.filter(Answer.group_id.in_(args['group_id']))
        result = ANSWERS_SCHEMA.dump(form_answers).data
        return result if result else ({"error": "no such row"}, status.HTTP_404_NOT_FOUND)
