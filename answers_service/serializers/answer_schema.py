"""marshmello app schema."""
from marshmallow import fields

from answers_service import MA


class AnswerSchema(MA.Schema):
    """output schema."""
    reply = fields.Str()
    user_id = fields.Integer()
    form_id = fields.Integer()
    field_id = fields.Integer()
    group_id = fields.Integer()

ANSWER_SCHEMA = AnswerSchema(strict=True)
ANSWERS_SCHEMA = AnswerSchema(many=True, strict=True)
