import os
from django.conf import settings
from urllib import unquote
import forms

def handle_upload(files, field_key, folder=''):
	upload_dir = settings.UPLOAD_PATH + str(folder)
	upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
	
	# Make sure the upload path exists, and create it if not.
	# Raises an OSError if the upload path does not exists
	if not os.path.exists(upload_full_path):
		os.makedirs(upload_full_path)

	upload = files[field_key]

	# Turn urlencodeded characters into normal characters
	upload.name = unquote(upload.name)

	# Append an underscore to the given filename until the name is unique
	while os.path.exists(os.path.join(upload_full_path, upload.name)):
		upload.name = '_' + upload.name
	dest = open(os.path.join(upload_full_path, upload.name), 'wb')
	
	# Write the uploaded file
	for chunk in upload.chunks():
		dest.write(chunk)
	dest.close()
	
	return os.path.join(upload_dir, upload.name)
	
def get_upload_url(request, submission):
	files = forms.get_answers(submission=submission, for_form=True, field=request.FILES.keys()[0])
	return os.path.join(settings.MEDIA_URL, files[request.FILES.keys()[0]])
