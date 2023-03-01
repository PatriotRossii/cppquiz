import re
import string
import random

from quiz.models import Question


def create_questions(nof_questions):
    for i in range(0, nof_questions):
        Question.objects.create(question=str(i), answer=str(i), result='OK', state='PUB',
                                hint=random_hint(), difficulty=1, explanation='because ' + str(i))


def get_question_pk(html):
    return int(re.findall("Question #(\d*)", html)[0])


def random_hint():
    return ''.join(random.sample(string.ascii_letters, 5))
