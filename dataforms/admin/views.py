from dataforms.models import Submission, Answer
from django.http import Http404
from django.shortcuts import render


def answers_view(request, submissionid):

    submission = Submission.objects.get(pk=submissionid)
    
    #answers = Answer.objects.get_answer_data(submissionid)
    
    cl = {
        'search_fields' : ['id', 'title']
    }
    
    vals = {
        'title'    : 'Answers for %s' % submission.slug,
        'answers' : '',
    }
    
    return render(request, 'admin/dataforms/answers.html', vals)

#def ajax_fiter_field(request, data_form):
#    
#    if request.is_ajax():
#       
#       
#        
#    else:
#        return Http404