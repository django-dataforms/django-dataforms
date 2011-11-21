from dataforms.utils.file import handle_upload
from dataforms.forms import create_form, create_collection
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os


def index(request):
	"""
	A demo page to show a form dynamically generated from the database. 
	"""
	
	form = create_form(request=request, form="personal-information", submission="myForm")

	if request.method == "POST":
		if form.is_valid():
			form.save()
			return redirect("index") 

	return render(request, "index.html", { 'form':form })


def form_collection(request):
	"""
	A demo page to show a form collection (many forms) dynamically generated from the database. 
	"""

	collection = create_collection(request=request, collection="test-collection", submission="myCollection", section="a")

	if request.method == "POST":
		if collection.is_valid():
			collection.save()
			return redirect("form_collection") 

	return render(request, 'collection.html', { 'forms':collection })


def upload(request):
	"""
	Handle files uploaded via AjaxUpload
	"""
	
	path = handle_upload(files=request.FILES, field_key=request.FILES.keys()[0], folder="1")
	return HttpResponse(os.path.join(settings.MEDIA_URL, path))
