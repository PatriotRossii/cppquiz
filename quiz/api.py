from django.http import Http404, JsonResponse

from quiz.models import Quiz


def quiz(request):
    quiz_key = request.GET.get('key')
    try:
        quiz = [q.id for q in Quiz.objects.get(key=quiz_key).get_ordered_questions()]
        return JsonResponse({'questions': quiz})
    except Quiz.DoesNotExist:
        raise Http404
