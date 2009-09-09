from django.conf import settings
import os

def handle_upload(files, field_key, submissionID):
	upload_dir = settings.UPLOAD_PATH + str(submissionID)
	upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
	
	if not os.path.exists(upload_full_path):
		os.makedirs(upload_full_path)

	upload = files[field_key]
	while os.path.exists(os.path.join(upload_full_path, upload.name)):
		upload.name = '_' + upload.name
	dest = open(os.path.join(upload_full_path, upload.name), 'wb')
	for chunk in upload.chunks():
		dest.write(chunk)
	dest.close()
	saved = os.path.join(upload_dir, upload.name)
	
	return saved
	
