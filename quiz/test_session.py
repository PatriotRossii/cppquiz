import mock
import unittest

from quiz.game_data import *
from quiz.models import *


class UserDataTest(unittest.TestCase):

    def test_given_new_session__has_no_correct_answers(self):
        session = {}
        s = UserData(session)
        self.assertSetEqual(set(), s.get_correctly_answered_questions())

    def test_given_new_session__after_a_correct_answer_to_a_published_question_is_registered__it_is_listed_as_answered(self):
        q1 = Question.objects.create(state='PUB', difficulty=1)
        q2 = Question.objects.create(state='PUB', difficulty=1)
        session = {}
        s = UserData(session)
        s.register_correct_answer(q1.pk)
        self.assertSetEqual({q1.pk}, s.get_correctly_answered_questions())
        s.register_correct_answer(q2.pk)
        self.assertSetEqual({q1.pk, q2.pk}, s.get_correctly_answered_questions())

    def test_given_new_session__after_a_correct_answer_to_a_retracted_question_is_registered__it_is_not_listed_as_answered(self):
        q = Question.objects.create(state='RET', difficulty=1)
        session = {}
        s = UserData(session)
        s.register_correct_answer(q.pk)
        self.assertSetEqual(set(), s.get_correctly_answered_questions())

    def test_given_new_session__after_a_published_question_becomes_retracted__its_answer_is_not_listed_as_answered(self):
        q = Question.objects.create(state='PUB', difficulty=1)
        session = {}
        s = UserData(session)
        s.register_correct_answer(q.pk)
        self.assertSetEqual({q.pk}, s.get_correctly_answered_questions())
        q.state = 'RET'
        q.save()
        self.assertSetEqual(set(), s.get_correctly_answered_questions())

    def test_given_existing_session__correct_answers_are_still_there(self):
        q = Question.objects.create(state='PUB', difficulty=1)
        old_data = UserData({})
        old_data.register_correct_answer(q.pk)
        session = {'user_data': old_data}
        new_data = UserData(session)
        self.assertSetEqual({q.pk}, new_data.get_correctly_answered_questions())

    def test_clear_correct_answers(self):
        q = Question.objects.create(state='PUB', difficulty=1)
        s = UserData({})
        s.register_correct_answer(q.pk)
        s.clear_correct_answers()
        self.assertSetEqual(set(), s.get_correctly_answered_questions())


class save_user_dataTest(unittest.TestCase):

    def test_sets_modified(self):
        session = mock.MagicMock()
        save_user_data(None, session)
        self.assertTrue(session.modified)

    def test_sets_user_data(self):
        q = Question.objects.create(state='PUB', difficulty=1)
        session = mock.MagicMock()
        user_data = UserData({})
        user_data.register_correct_answer(q.pk)
        save_user_data(user_data, session)
        session.__setitem__.assert_called_once_with('user_data', user_data)

    def test_sets_expiry(self):
        session = mock.MagicMock()
        save_user_data(None, session)
        session.set_expiry.assert_called_once_with(315360000)
