from annoying.decorators import JsonResponse
from dataforms.models import Submission, Answer, Field, DataFormField, \
    FieldChoice
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import simplejson


def answers(request, submissionid):

    submission = Submission.objects.get(pk=submissionid)
    answers = Answer.objects.get_answer_data(submissionid)
    
    vals = {
        'title'    : 'Answers for %s' % submission.slug,
        'answers' : answers,
    }
    
    return render(request, 'admin/dataforms/answers.html', vals)


def ajax_filter(request, object):
    
    #Return 404 if not an ajax request
    if not request.is_ajax():
        raise Http404
    
    values = []
    order = []
    filter = {}
    
    if request.GET.has_key('values'):
        values = request.GET['values'].split(',')
    
    if request.GET.has_key('order'):
        order = request.GET['order'].split(',')

    for key, value in request.GET.iteritems():
        if key != 'order' and key !='values':
            filter[str(key)] = str(value)
    
    try:    
        model_class = ContentType.objects.get(app_label="dataforms", model=object).model_class()
        queryset = model_class.objects.values(*values).order_by(*order).filter(**filter)
    
    except:
        return JsonResponse(0)
        
    return JsonResponse(list(queryset))
    

class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')
