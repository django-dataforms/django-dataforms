import os
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from dataforms.forms import create_form, create_collection
from dataforms.file_handler import get_upload_url, handle_upload
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
	"""
	A demo page to show a form dynamically generated from the database. 
	"""
	
	form = create_form(request=request, form="personal-information", submission="myForm")
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/") 

	return render_to_response("index.html", { 'form':form }, RequestContext(request))

def form_collection(request):
	"""
	A demo page to show a form collection (many forms) dynamically generated from the database. 
	"""

	collection = create_collection(request=request, collection="test-collection", submission="myCollection", section="a")

	if request.method == "POST":
		if collection.is_valid():
			collection.save()
			return HttpResponseRedirect("/collection/") 

	return render_to_response('collection.html', { 'forms':collection }, RequestContext(request))

def upload(request):
	"""
	Handle files uploaded via AjaxUpload
	"""
	
	path = handle_upload(files=request.FILES, field_key=request.FILES.keys()[0], folder="1")
	return HttpResponse(os.path.join(settings.MEDIA_URL, path))
