from django.test import TestCase, Client
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q

from .forms import _field_for_form, get_answers # kind of breaking low coupling here
from .models import Submission, Answer
from .settings import BOOLEAN_FIELDS, MULTI_CHOICE_FIELDS, SINGLE_CHOICE_FIELDS

class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.
    
    Usage::
    
	    rf = RequestFactory()
	    get_request = rf.get('/hello/')
	    post_request = rf.post('/submit/', {'foo': 'bar'})
    
    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client
    
    Once you have a request object you can pass it to any view function, 
    just as if that view had been hooked up using a URLconf.
    
    Original From: http://www.djangosnippets.org/snippets/963/
    
    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)

class CustomTestCase(TestCase):
	def assertValidSave(self, data, submission):
		"""
		Asserts that data from a POST request was saved correctly in the DB.
		We can't compare them directly because we need to mash the DB data
		back into a form that is comparable to request.POST data.
		
		:param data: request.POST data
		:param submission: a Submission object or slug
		"""
		
		# Slightly evil, do type checking to see if submission is a Submission object or string
		if isinstance(submission, str):
			submission = Submission.objects.get(slug=submission)
		answers_to_compare = get_answers(submission=submission, for_form=True)
		
		# ------ 1 ------
		# This fixes the fact that a POST request will not have a checkbox key,
		# but the DB _will_ contain a blank string for a checkbox false value.
		
		# Get the boolean field answers
		answers = Answer.objects.select_related('field').filter(
			submission=submission,
			field__field_type__in=BOOLEAN_FIELDS
		)
		boolean_field_names = [(answer.data_form.slug, answer.field.slug) for answer in answers]
		
		# For every boolean field, remove these from the DB answers because
		# they will not exist in the form POST
		for form_name, field_name in boolean_field_names:
			del answers_to_compare[_field_for_form(name=field_name, form=form_name)]
			
		# ------ 2 ------
		# This fixes the fact that each request.POST element will be a list
		# and that won't be true from get_answers
		
		# Get all Answers that won't be lists
		answers = Answer.objects.select_related('field').filter(
			submission=submission
		).exclude(Q(field__field_type__in=MULTI_CHOICE_FIELDS)	| Q(field__field_type__in=BOOLEAN_FIELDS))
		
		field_names = [(answer.data_form.slug, answer.field.slug) for answer in answers]
		
		# Wrap them as lists
		for form_name, field_name in field_names:
			form_field_name = _field_for_form(name=field_name, form=form_name)
			answers_to_compare[form_field_name] = [answers_to_compare[form_field_name]]
		
		# ------ 3 ------
		# Actually compare the submitted data to the DB data
		self.assertEqual(data, answers_to_compare)
		
			
		
		