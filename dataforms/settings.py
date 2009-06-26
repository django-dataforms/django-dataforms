"""
App Settings
============

This file should not be updated.  Instead, please put any additional field mappings
in your project settings file.  That way any custom fields and widgets will be
de-coupled from this app.

:constant FIELD_MAPPINGS: a dictionary of form fields are available to be used.
:constant ADMIN_SORT_JS: tuple that references the custom javascript for the django admin.
:constant FIELD_TYPE_CHOICES: tuple that is used by the model as choices

:constant BOOLEAN_FIELDS: an element of FIELD_MAPPINGS that should be interpreted
	on save as only yes/no
:constant SINGLE_CHOICE_FIELDS = field types that have choices, but only one selected
	on save, for Select boxes or a single RadioSelect type
:constant MULTI_CHOICE_FIELDS = field types that have choices and multiple
	ones can be selected on save, for SelectMultiple boxes or CheckboxSelectMultiple
:constant CHOICE_FIELDS: both SINGLE_CHOICE_FIELDS and MULTI_CHOICE_FIELDS  
"""

from django.conf import settings
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

FIELD_MAPPINGS = {}

if hasattr(settings, 'FIELD_MAPPINGS'):
	FIELD_MAPPINGS = settings.FIELD_MAPPINGS


# Make sure to specify a 'widget' for every FIELD_MAPPING entry
FIELD_MAPPINGS.update( {
	'TextInput' : { 'class':forms.CharField, 'widget':forms.TextInput },
	'Textarea' : { 'class':forms.CharField, 'widget':forms.Textarea },
	'Select' : { 'class':forms.ChoiceField, 'widget':forms.Select },
	'SelectMultiple' : { 'class':forms.MultipleChoiceField, 'widget' : forms.SelectMultiple },
	'RadioSelect' : { 'class':forms.ChoiceField, 'widget':forms.RadioSelect },
	'Password' : { 'class':forms.CharField, 'widget':forms.PasswordInput },
	'Email' : { 'class':forms.EmailField, 'widget':forms.TextInput },
	'DateField' : { 'class':forms.DateField, 'widget':AdminDateWidget },
	'CheckboxInput' : { 'class':forms.BooleanField, 'widget':forms.CheckboxInput },
	'CheckboxSelectMultiple' : { 'class':forms.MultipleChoiceField, 'widget':forms.CheckboxSelectMultiple },
} )

BOOLEAN_FIELDS = ('CheckboxInput',)
SINGLE_CHOICE_FIELDS = ('Select', 'RadioSelect')
MULTI_CHOICE_FIELDS = ('SelectMultiple', 'CheckboxSelectMultiple')
CHOICE_FIELDS = SINGLE_CHOICE_FIELDS + MULTI_CHOICE_FIELDS  

FIELD_DELIMITER = "__"

if hasattr(settings, 'ADMIN_SORT_JS'):
	ADMIN_SORT_JS = settings.ADMIN_SORT_JS
else:
	ADMIN_SORT_JS = (
		'https://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
		'https://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
		'%s/scripts/jquery.adminmenusort.js' % settings.MEDIA_URL,
	)

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])
