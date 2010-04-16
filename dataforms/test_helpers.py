from django.test import TestCase, Client
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q

from .forms import _field_for_form, get_answers # kind of breaking low coupling here
from .models import Submission, Answer
from .settings import BOOLEAN_FIELDS, MULTI_CHOICE_FIELDS, UPLOAD_FIELDS

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
	def assertDictionaryEqual(self, from_post, from_db):
		"""
		Just a nicer way to see out dictionary differences
		"""
		
		messages = []
		
		for key in from_post:
			if not from_db.has_key(key):
				messages.append("In form POST, but not present in database: %s" % key)
			elif from_post[key] != from_db[key]:
				messages.append("POST %s NOT EQUAL DB: %s != %s" % (key, repr(from_post[key]), repr(from_db[key])))
				
		for key in from_db:
			if not from_post.has_key(key) and from_db[key]:
				messages.append("NOT PRESENT IN FORM POST: %s, BUT HAD DB DATA: %s" % (key, repr(from_db[key])))
				
		return self.fail("\n" + "\n".join(messages)) if messages else None
	
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
		answers_from_db = get_answers(submission=submission, for_form=True)
		
		# ------ 1 ------
		# This fixes the fact that a POST request will not have a checkbox key,
		# but the DB _may_ contain a blank string for a checkbox False value
		# and _will_ contain a '1' for a checkbox True value.
				
		# Get the boolean field answers
		answers = Answer.objects.select_related('field').filter(
			submission=submission,
			field__field_type__in=BOOLEAN_FIELDS
		)
		boolean_field_names = [(answer.data_form.slug, answer.field.slug) for answer in answers]
		
		# For boolean fields that aren't checked, remove these from the DB answers because
		# they will not exist in the form POST
		for form_name, field_name in boolean_field_names:
			key = _field_for_form(name=field_name, form=form_name)
			if data.has_key(key) and not data[key]:
				# Checkbox was not checked, delete element containing *blank string* in DB returned answers
				# to make these "equal" for testing
				del answers_from_db[key]
			elif data.has_key(key) and data[key]:
				# Checkbox was checked, so DB has "1" and post has "[1]" ... make these "equal" for testing
				answers_from_db[key] = [answers_from_db[key]]
		
		# ------ 2 ------
		# This fixes the fact that each request.POST element will be a list
		# and that won't be true from get_answers
		
		# Get all Answers that won't be lists
		# FIXME: excluding upload fields here. Once testing is implemented, remove +UPLOAD_FIELDS
		answers = Answer.objects.select_related('field').filter(
			submission=submission
		).exclude(Q(field__field_type__in=MULTI_CHOICE_FIELDS+BOOLEAN_FIELDS+UPLOAD_FIELDS))
		
		field_names = [(answer.data_form.slug, answer.field.slug) for answer in answers]
		
		# Wrap them as lists
		for form_name, field_name in field_names:
			form_field_name = _field_for_form(name=field_name, form=form_name)
			try:
				answers_from_db[form_field_name] = [answers_from_db[form_field_name]]
			except KeyError:
				self.fail("It looks like get_answers() (or saving) might be borked. '%s' was supposed to exist in answers_from_db, but doesn't. Perhaps a certain storage mechanism in the save() function is not working properly? Or you messed with the fields and haven't updated TEST_FORM_POST_DATA?" % form_field_name)
		
		# ------ 3 ------
		# Actually compare the submitted data to the DB data
		self.assertDictionaryEqual(from_post=data, from_db=answers_from_db)
		
