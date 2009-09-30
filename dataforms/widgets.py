from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
#from datetime import date

class NoteWidget(forms.Widget):
	def render(self, name, value, attrs=None):
		return ""
	   
class FileWidget(forms.FileInput):
	"""
	A FileField Widget that shows its current value if it has one.
	"""
	def __init__(self, attrs={}):
		super(FileWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		output = []
		output.append(super(FileWidget, self).render(name, value, attrs))
		if value:
			# FIXME:  Possible figure out a way to dynamically pass widget arguments to create the proper file path.
			#if hasattr(value, "name"):
			#	value = "/".join([date.today().strftime(settings.UPLOAD_PATH), value.name])
			
			output.append('<div class="cfile">%s <a target="_blank" href="%s">%s</a></div>' % \
				('Currently:', '/'.join([settings.MEDIA_URL, value]), value))
		return mark_safe(u''.join(output))