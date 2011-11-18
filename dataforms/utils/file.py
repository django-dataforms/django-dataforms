from dataforms.app_settings import FILE_UPLOAD_PATH
from django.conf import settings
from django.core.files.base import File
from django.utils.encoding import smart_str
from urllib import unquote
import os


class DataFormFile(File):
	"""
	Data Form File object that is used for FileField obecjts to represent a file.
	"""
	
	def __init__(self, file, name=None):
		super(DataFormFile, self).__init__(file, name)
		self.path_name = self.name
		self.name = self.name.split('/')[-1]
		
	
	def _get_url(self):
		return ''.join([settings.MEDIA_URL, self.path_name])
	url = property(_get_url)


def handle_upload(files, field_key, folder=''):
	upload = files[field_key]
	upload_dir = FILE_UPLOAD_PATH + str(folder)
	upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

	# If the upload is of type DataFormFile, then we know
	# that this is a file that already exists, we don't need to upload anything.
	if upload.__class__.__name__ == 'DataFormFile':
		return upload.path_name
	
	# Make sure the upload path exists, and create it if not.
	# Raises an OSError if the upload path does not exists
	if not os.path.exists(upload_full_path):
		os.makedirs(upload_full_path)


	# Turn urlencodeded characters into normal characters and wrap
	# it with smart_str for foreign characters
	upload.name = smart_str(unquote(upload.name))

	# Append an underscore to the given filename until the name is unique
	while os.path.exists(os.path.join(upload_full_path, upload.name)):
		upload.name = '_' + upload.name
	dest = open(os.path.join(upload_full_path, upload.name), 'wb')
	
	# Write the uploaded file
	for chunk in upload.chunks():
		dest.write(chunk)
	dest.close()
	
	return os.path.join(upload_dir, upload.name)
