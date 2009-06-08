from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from dataforms.forms import create_form, create_form_collection, _create_form
from dataforms.models import Submission, DataForm
from itertools import chain
from django.db import connection, transaction

@transaction.commit_on_success
def form(request):
	"""
	A demo page to show a form dynamically generated from the database. 
	"""
	
	form = create_form(request=request, form='personal-information', submission="myForm")
	
	if request.method == "POST":
		# They have submitted the form
		if form.is_valid():
			# Save the form. Automagically creates a submission if it doesn't exist
			# and associates the submission to the right data_forms
			form.save()
	
	vals = {
		'form':form,
	}
	
	return render_to_response('index.html', vals, RequestContext(request))

@transaction.commit_on_success
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