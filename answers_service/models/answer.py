""" answers service model """
import datetime

from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint

from answers_service.db import DB


class Answer(DB.Model):  # pylint: disable=too-few-public-methods
    """models."""
    reply = Column(String(200), nullable=False)
    user_id = Column(Integer(), nullable=False)
    form_id = Column(Integer(), nullable=False)
    field_id = Column(Integer(), nullable=False)
    group_id = Column(Integer(), nullable=False)
    answer_date = Column(DateTime(), default=datetime.datetime.utcnow)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'form_id', 'field_id', name='answer_pk'),)
