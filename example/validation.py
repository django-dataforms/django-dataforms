"""
Validation
==========

This is really freakn sweet!
"""

from django import forms
from django.template.defaultfilters import filesizeformat
from dataforms import app_settings

class BaseValidationForm(object):
	pass

class PersonalInformationForm(BaseValidationForm):
	@staticmethod
	def clean_uploader(self):
		
		content = self.cleaned_data['personal-information__uploader']
	 	if content._size > app_settings.MAX_UPLOAD_SIZE:
	 		raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % (filesizeformat(app_settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
	 	return content
