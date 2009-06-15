from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from dataforms.forms import create_form, create_collection, _create_form
from dataforms.models import Submission, DataForm
from itertools import chain
from django.db import connection

def index(request):
	"""
	A demo page to show a form dynamically generated from the database. 
	"""
	
	form = create_form(request=request, form="personal-information", submission="myForm")
	
	if request.method == "POST":
		if form.is_valid():
			# Creates a Submission and saves the submitted form data
			form.save()
	
	vals = {
		'form':form,
	}
	
	return render_to_response("index.html", vals, RequestContext(request))

def form_collection(request):
	"""
	A demo page to show a form collection (many forms) dynamically generated from the database. 
	"""

	form_collection = create_collection(request=request, collection="test-collection", submission="myCollection")

	if request.method == "POST":
		if form_collection.is_valid():
			# Creates a Submission and saves the submitted form data
			form_collection.save()

	vals = {
		'forms':form_collection,
	}

	return render_to_response('collection.html', vals, RequestContext(request))