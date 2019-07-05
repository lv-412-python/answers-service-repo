"""Tests for form service."""
from unittest import main
from flask_testing import TestCase
from answers_service import APP
from answers_service.db import DB
from answers_service.models.answer import Answer
from answers_service.config.test_config import TestConfiguration


def create_app(config_obj):
    """
    Creates Flask app with configuration, you need.
    :param config_obj: name of configuration.
    :return: flask app.
    """
    app = APP
    app.config.from_object(config_obj)
    return app


class FormAnswersTest(TestCase):
    """Tests for get resource."""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        answer1 = Answer(reply="Reply 1", user_id=1, form_id=1, field_id=1, group_id=1)
        answer2 = Answer(reply="Reply 2", user_id=2, form_id=2, field_id=2, group_id=2)
        DB.session.add(answer1)
        DB.session.add(answer2)
        DB.session.commit()
        id1 = Answer.query.filter_by(reply="Reply 1", user_id=1).first()
        self.user_id = id1.user_id
        self.form_id_1 = id1.form_id
        id2 = Answer.query.filter_by(reply="Reply 2", user_id=2).first()
        self.forms_id_2 = id2.form_id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/answers/form/{}'.format(self.form_id_1))
            check = [{
                "reply": "Reply 1",
                "user_id": self.user_id,
                "form_id": self.form_id_1,
                "field_id": 1,
                "group_id": 1
            }]
            self.assertEqual(response.json, check)

    def test_get_no_form(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/answers/form/2222')
            self.assertEqual(response.json, {"error": "no such row"})


class GroupAnswersTest(TestCase):
    """Tests for get group answers"""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        answer1 = Answer(reply="Reply 1", user_id=1, form_id=1, field_id=1, group_id=1)
        answer2 = Answer(reply="Reply 2", user_id=2, form_id=2, field_id=2, group_id=2)
        DB.session.add(answer1)
        DB.session.add(answer2)
        DB.session.commit()
        id1 = Answer.query.filter_by(reply="Reply 1", user_id=1).first()
        self.user_id = id1.user_id
        self.form_id_1 = id1.form_id
        self.group_id_1 = id1.group_id

        id2 = Answer.query.filter_by(reply="Reply 2", user_id=2).first()
        self.forms_id_2 = id2.form_id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/answers/group/{}/{}'.format(self.form_id_1, self.group_id_1))
            check = [{
                "reply": "Reply 1",
                "user_id": self.user_id,
                "form_id": self.form_id_1,
                "field_id": 1,
                "group_id": self.group_id_1
            }]
            self.assertEqual(response.json, check)

    def test_get_no_group(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/answers/group/10/10')
            self.assertEqual(response.json, {"error": "no such row"})


class PostAnswerTest(TestCase):
    """Tests for get group answers"""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables."""
        DB.create_all()

    def test_post_success(self):
        """Tests post resource success."""
        with self.create_app().test_client() as client:
            response = client.post('/answers/new',
                                   json=[{
                                          "group_id": 1,
                                          "field_id": 1,
                                          "reply": "AMAZING!",
                                          "user_id": 1,
                                          "form_id": 1
                                         },
                                         {
                                          "group_id": 1,
                                          "field_id": 1,
                                          "reply": "AMAZING!",
                                          "user_id": 2,
                                          "form_id": 1
                                         }])
            self.assertEqual(response.status_code, 200)

    def test_post_failure(self):
        """Tests post resource failure."""
        with self.create_app().test_client() as client:
            client.post('/answers/new', json=[{
                                          "group_id": 1,
                                          "field_id": 1,
                                          "reply": "AMAZING!",
                                          "user_id": 1,
                                          "form_id": 1
                                         },
                                         {
                                          "group_id": 1,
                                          "field_id": 1,
                                          "reply": "AMAZING!",
                                          "user_id": 2,
                                          "form_id": 1
                                         }])
            response = client.post('/answers/new',
                                   json=[{
                                       "group_id": 1,
                                       "field_id": 1,
                                       "reply": "AMAZING!",
                                       "user_id": 1,
                                       "form_id": 1
                                   },
                                       {
                                           "group_id": 1,
                                           "field_id": 1,
                                           "reply": "AMAZING!",
                                           "user_id": 2,
                                           "form_id": 1
                                       }])
            self.assertEqual(response.json, {"error": "this answer alreasy exist"})
            self.assertEqual(response.status_code, 203)

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

if __name__ == '__main__':
    main()