from answer import Answer
from models import Quiz

class QuestionStats:
    def __init__(self, skipped=False, attempts=0, used_hint=False):
        self.skipped = skipped
        self.attempts = attempts
        self.used_hint = used_hint

    def score(self):
        score = self.skipped == False
        if self.used_hint:
            score -= .5
        score *=  pow(.5, self.attempts)
        return score

class QuizInProgress:
    def __init__(self, session, quiz):
        self.session = session
        self.quiz = quiz
        if session.has_key('quiz_in_progress') and session['quiz_in_progress'].quiz.key == quiz.key:
            other = session['quiz_in_progress']
            self.answers = other.answers
            self.previous_result = other.previous_result
            self.attempts = other.attempts
            self.used_hint = other.used_hint
        else:
            self.answers = []
            self._reset_question_state()

    def get_current_question(self):
        return self.quiz.questions.all()[len(self.answers)]

    def get_previous_result(self):
        return self.previous_result

    def nof_answered_questions(self):
        return len(self.answers)

    def get_total_nof_questions(self):
        return self.quiz.questions.count()

    def is_finished(self):
        return self.quiz.questions.count() == self.nof_answered_questions()

    def score(self):
        return float(sum([q.score() for q in self.answers]))

    def answer(self, request):
        answer = Answer(self.get_current_question(), request)
        if answer.correct:
            self.answers.append(QuestionStats(attempts=self.attempts, used_hint=self.used_hint))
            self._reset_question_state()
            self.previous_result = 'correct'
        else:
            self.previous_result = 'incorrect'
            self.attempts += 1
        return

    def use_hint(self):
        self.used_hint = 1

    def skip(self):
        self._reset_question_state()
        self.answers.append(QuestionStats(skipped=True))

    def save(self):
        self.session.modified = True
        self.session['quiz_in_progress'] = self
        self.session.set_expiry(60*60*24*365*10) #TODO akn DRY

    def _reset_question_state(self):
        self.previous_result = None
        self.attempts = 0
        self.used_hint = 0


def clear_quiz_in_progress(session):
    if session.has_key('quiz_in_progress'):
        session.pop('quiz_in_progress')