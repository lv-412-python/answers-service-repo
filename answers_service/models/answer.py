""" answers service model """
from sqlalchemy import Column, Integer, String
from answers_service.db import DB


class Answer(DB.Model):  # pylint: disable=too-few-public-methods
    """ models """
    extend_existing = True
    id = Column(Integer(), primary_key=True, autoincrement=True)
    reply = Column(String(200), nullable=False)
    user_id = Column(Integer(), nullable=False)
    form_id = Column(Integer(), nullable=False)
    field_id = Column(Integer(), nullable=False)
    group_id = Column(Integer(), nullable=False)

    def __repr__(self):
        return f"Answer(id = {self.id}, reply = {self.reply},user_id = " \
            f"{self.form_id}, form_id = {self.form_id}, field_id = {self.field_id})" \
            f", group_id = {self.group_id}"
