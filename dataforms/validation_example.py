"""
Validation
==========

This is really freakn sweet!
"""

from django import forms

class BaseValidationForm(object):
	@staticmethod
	def clean(self):
		raise forms.ValidationError('clean base error')

class PersonalInformationForm(BaseValidationForm):
	@staticmethod
	def clean(self):
		raise forms.ValidationError('clean error')
	
	@staticmethod
	def clean_textbox(self):
		raise forms.ValidationError('clean field error')
