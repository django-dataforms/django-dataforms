"""
Default settings file.  

This file should not be updated.  Instead, please put any additional field mappings
in your project settings file.  That way any custom fields and widgets will be
de-coupled from this app.

:constant FIELD_MAPPINGS: a dictionary of form fields are available to be used.
:constant ADMIN_SORT_JS: tuple that references the custom javascript for the django admin.
:constant FIELD_TYPE_CHOICES: tuple that is used by the model as choices  
"""
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.conf import settings

FIELD_MAPPINGS = {}

if hasattr(settings, 'FIELD_MAPPINGS'):
	FIELD_MAPPINGS = settings.FIELD_MAPPINGS

FIELD_MAPPINGS.update( {
	'TextInput' : { 'class':forms.CharField },
	'Textarea' : { 'class':forms.CharField, 'widget':forms.Textarea },
	'Select' : { 'class':forms.ChoiceField },
	'SelectMultiple' : { 'class':forms.MultipleChoiceField },
	'RadioSelect' : { 'class':forms.ChoiceField, 'widget':forms.RadioSelect },
	'Password' : { 'class':forms.CharField, 'widget':forms.PasswordInput },
	'Email' : { 'class':forms.EmailField },
	'DateField' : { 'class':forms.DateField, 'widget':AdminDateWidget },
	'CheckboxInput' : { 'class':forms.BooleanField, 'widget':forms.CheckboxInput },
	'CheckboxSelectMultiple' : { 'class':forms.MultipleChoiceField, 'widget':forms.CheckboxSelectMultiple },
} )

# You need to import your django settings to get the MEDIA_URL for this to work.
ADMIN_SORT_JS = (
	'https://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
	'%s/scripts/jquery.adminmenusort.js' % settings.MEDIA_URL,
)

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])