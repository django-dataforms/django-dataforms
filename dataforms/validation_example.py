"""
Validation
==========

This is really freakn sweet!
"""

from django import forms

class BaseValidationForm(object):
	@staticmethod
	def clean_frogs(self):
		#pass
		data = self.cleaned_data['frogs']
		raise forms.ValidationError('this is a FROG ERROR error')
		return data
		

