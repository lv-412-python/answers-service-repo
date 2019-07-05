""" answers service model """
from sqlalchemy import Column, Integer, String
from answers_service.db import DB


class Answer(DB.Model):  # pylint: disable=too-few-public-methods
    """ models """
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    reply = Column(String(200), nullable=False)
    user_id = Column(Integer(), nullable=False)
    form_id = Column(Integer(), nullable=False)
    field_id = Column(Integer(), nullable=False)
    group_id = Column(Integer(), nullable=False)
