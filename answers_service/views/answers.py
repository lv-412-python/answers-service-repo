"""methods classes."""
from flask import request, Response
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError, fields
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import parser
import requests

from answers_service import APP
from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.serializers.answer_schema import ANSWERS_SCHEMA, ANSWER_SCHEMA


class UserAnswer(Resource):
    """User answers."""
    def post(self):
        """creates new answer.
        :return json: new answer
        """
        for answer in request.get_json():
            try:
                new_answer = ANSWER_SCHEMA.load(answer).data
            except ValidationError as err:
                APP.logger.error('invalid input')
                return err.messages, status.HTTP_400_BAD_REQUEST
            add_new_answer = Answer(**new_answer)
            DB.session.add(add_new_answer)
            try:
                DB.session.commit()
            except IntegrityError:
                APP.logger.error('%s already exist.', answer)
                DB.session.rollback()
                return {'error': 'Already exists.'}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_201_CREATED)

    def get(self):
        """gets all answers of the form.
        :return json: answers"""
        url_args = {
            'form_id': fields.Int(required=True, validate=lambda val: val > 0),
            'group_id': fields.List(fields.Int(validate=lambda val: val > 0)),
            'user_id':  fields.Int(validate=lambda val: val > 0),
            'from_date': fields.Date(),
            'end_date': fields.Date()
        }
        try:
            args = parser.parse(url_args, request)
        except HTTPException:
            APP.logger.error('%s not correct URL', request.url)
            return {"error": "Invalid URL."}, status.HTTP_400_BAD_REQUEST
        form_answers = Answer.query.filter(Answer.form_id == args['form_id'])\
            .order_by(Answer.field_id)
        if 'from_date' in args:
            form_answers = form_answers.filter(Answer.answer_date >= args['from_date'])
        if 'end_date' in args:
            form_answers = form_answers.filter(Answer.answer_date <= args['end_date'])
        if 'user_id' in args:
            form_answers = form_answers.filter(Answer.user_id == args['user_id'])
        if 'group_id' in args:
            groups = {'group_id': args['group_id']}
            # get_groups = requests.get('http://groups-service:5050/group', params=groups)
            get_groups = requests.get('http://0.0.0.0:5000/group', params=groups)
            group_members = []
            for group in get_groups.json():
                group_members.extend(group['members'])
            form_answers = form_answers.filter(Answer.user_id.in_(set(group_members)))
            if '/statistic' in request.url_rule.rule:
                users_to_answer = len(group_members)
                answered = set()
                result = ANSWERS_SCHEMA.dump(form_answers).data
                for answer in result:
                    answered.add(answer["user_id"])
                return {"users": users_to_answer, "answered": len(answered)}
        result = ANSWERS_SCHEMA.dump(form_answers).data
        return (result, status.HTTP_200_OK) if result else \
               ({"error": "Does not exist."}, status.HTTP_404_NOT_FOUND)
