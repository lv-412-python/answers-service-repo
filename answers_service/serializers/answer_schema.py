""" marshmello app schema """
from answers_service import MA

# answer schema
class AnswerSchema(MA.Schema):
    """ output schema """
    class Meta:  # pylint: disable=too-few-public-methods
        """ output """
        fields = ('reply', 'user_id', 'form_id', 'field_id', 'group_id')


# init answer schema
ANSWER_SCHEMA = AnswerSchema(strict=True)
ANSWERS_SCHEMA = AnswerSchema(many=True, strict=True)
