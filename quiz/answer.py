from quiz.models import UsersAnswer


class Answer:
    def __init__(self, question, request):
        self.question = question
        self.given_answer = request.GET.get('answer', '').strip()
        self.given_result = request.GET.get('result', '').strip()
        self.correct = self.given_result == self.question.result and\
            (self.question.result != 'OK' or self.given_answer == self.question.answer.strip())

    def register_given_answer(self):
        UsersAnswer.objects.create(
            question=self.question,
            answer=self.given_answer,
            result=self.given_result,
            correct=self.correct)
