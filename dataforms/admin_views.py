from django.shortcuts import render
from models import Submission, Answer


def answers_view(request, submissionid):

    submission = Submission.objects.get(pk=submissionid)
    
    answers = Answer.objects.get_answer_data(submissionid)
    
    cl = {
        'search_fields' : ['id', 'title']
    }
    
    vals = {
        'title'    : 'Answers for %s' % submission.slug,
        'answers' : answers,
    }
    
    return render(request, 'admin/dataforms/answers.html', vals)