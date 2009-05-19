from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from dataforms.forms import create_form, create_form_collection, _create_form
from itertools import chain
from django.db import connection

def form(request):

	form = create_form(request, 'personal-information')
	
	if form.is_valid():
		pass
	
	
	vals = {
		'form':form,
		#'x':x,
		#'z':z,
	}
	
	return render_to_response('index.html', vals, RequestContext(request))


#TODO
def form_collection(request):

	form_collection = create_form_collection('irb')

	assert False

	if request.method == 'POST':

		form = FormClass(request.POST, request.FILES)

		if form.is_valid():
			pass
			#form.clean('me')

			#return HttpResponseRedirect('/')


	else:
		form = FormClass()

	vals = {
		'form':form,
		#'x':x,
		#'z':z,
	}

	return render_to_response('index.html', vals, RequestContext(request))