from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from dataforms.forms import create_form, create_form_collection, _create_form
from dataforms.models import Submission
from itertools import chain
from django.db import connection

def form(request):
	"""
	A demo page to show a form dynamically generated
	from the database. 
	"""
	
	try:
		submission = Submission.objects.get(slug="myForm")
	except Submission.DoesNotExist:
		submission = Submission.objects.create(slug="myForm")
	
	form = create_form(request=request, slug='personal-information', submission=submission)
	
	if form.is_valid():
		form.save(submission=submission)
	
	vals = {
		'form':form,
	}
	
	return render_to_response('index.html', vals, RequestContext(request))

def form_collection(request):
	"""
	A demo page to show a form collection (many forms)
	dynamically generated from the database. 
	"""

	# FIXME: finish code 

	form_collection = create_form_collection('irb')

	if request.method == 'POST':
		form = FormClass(request.POST, request.FILES)

		if form.is_valid():
			pass
	else:
		form = FormClass()

	vals = {
		'form':form,
	}

	return render_to_response('index.html', vals, RequestContext(request))