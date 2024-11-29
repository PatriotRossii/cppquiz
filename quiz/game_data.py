from collections import defaultdict

from quiz.models import Question
from quiz.util import save_data_in_session


class UserData:
    def __init__(self, session):
        if 'user_data' in session:
            self.correctly_answered = set(session['user_data'].get('correctly_answered', []))
            self.dismissed_training_msg = session['user_data'].get('dismissed_training_msg', False)
            self.attempts = defaultdict(int, session['user_data'].get('attempts', {}))
        else:
            self.correctly_answered = set()
            self.dismissed_training_msg = False
            self.attempts = defaultdict(int)

    def get_correctly_answered_questions(self):
        return set(Question.objects.filter(pk__in=self.correctly_answered, state='PUB').values_list('pk', flat=True))

    def register_correct_answer(self, question_id):
        self.correctly_answered.add(question_id)

    def clear_correct_answers(self):
        self.correctly_answered.clear()

    def dismiss_training_msg(self):
        self.dismissed_training_msg = True

    def register_attempt(self, answer):
        self.attempts[int(answer.question.pk)] += 1

    def attempts_given_for(self, question_id):
        return self.attempts[int(question_id)]

    def to_dict(self):
        return {"correctly_answered": list(self.correctly_answered), "dismissed_training_msg": self.dismissed_training_msg, "attempts": self.attempts}


def save_user_data(user_data, session):
    save_data_in_session({'user_data': user_data.to_dict()}, session)
