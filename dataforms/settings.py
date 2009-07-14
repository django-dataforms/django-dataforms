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
:constant SINGLE_NUMBER_FIELDS: For fields that need pseudo-foreign key storage
:constant MULTI_NUMBER_FIELDS: For fields that need pseudo-many-to-many storage
"""

from django.conf import settings

FIELD_MAPPINGS = {}

if hasattr(settings, 'FIELD_MAPPINGS'):
	FIELD_MAPPINGS = settings.FIELD_MAPPINGS
	
# Make sure to specify a 'widget' for every FIELD_MAPPING entry
FIELD_MAPPINGS.update( {
	'TextInput' : { 'class': 'django.forms.CharField', 'widget': 'django.forms.TextInput' },
	'Textarea' : { 'class': 'django.forms.CharField', 'widget': 'django.forms.Textarea' },
	'Select' : { 'class': 'django.forms.ChoiceField', 'widget' : 'django.forms.Select' },
	'SelectMultiple' : { 'class': 'django.forms.MultipleChoiceField', 'widget' : 'django.forms.SelectMultiple' },
	'RadioSelect' : { 'class': 'django.forms.ChoiceField', 'widget' : 'django.forms.RadioSelect' },
	'Password' : { 'class': 'django.forms.CharField', 'widget' : 'django.forms.PasswordInput' },
	'Email' : { 'class': 'django.forms.EmailField', 'widget' : 'django.forms.TextInput' },
	'DateField' : { 'class': 'django.forms.DateField', 'widget': 'django.contrib.admin.widgets.AdminDateWidget' },
	'CheckboxInput' : { 'class': 'django.forms.BooleanField', 'widget' : 'django.forms.CheckboxInput' },
	'CheckboxSelectMultiple' : { 'class': 'django.forms.MultipleChoiceField', 'widget' : 'django.forms.CheckboxSelectMultiple' },
} )

# Process the field mappings and import any modules specified by string name
for key in FIELD_MAPPINGS:
	# Replace the string arguments with the actual modules or classes
	for sub_key in ('class', 'widget'):
		value = FIELD_MAPPINGS[key][sub_key]
		
		if isinstance(value, str) or isinstance(value, unicode):
			names = value.split(".")
			module_name = ".".join(names[:-1])
			class_name = names[-1]
			module = __import__(module_name, fromlist=[class_name])
			
			# Replace the string with a class pointer
			FIELD_MAPPINGS[key][sub_key] = getattr(module, class_name)

	# Handle widget arguments
	if not FIELD_MAPPINGS[key].has_key('widget_kwargs'):
		# Initialize all field-mappings that don't have a 'widget_kwargs' key
		FIELD_MAPPINGS[key]['widget_kwargs'] = {}

BOOLEAN_FIELDS = getattr(settings, "BOOLEAN_FIELDS", ()) + ('CheckboxInput',)
SINGLE_CHOICE_FIELDS = getattr(settings, "SINGLE_CHOICE_FIELDS", ()) + ('Select', 'RadioSelect')
MULTI_CHOICE_FIELDS = getattr(settings, "MULTI_CHOICE_FIELDS", ()) + ('SelectMultiple', 'CheckboxSelectMultiple')
CHOICE_FIELDS = getattr(settings, "CHOICE_FIELDS", ()) + (SINGLE_CHOICE_FIELDS + MULTI_CHOICE_FIELDS)

# This is for pseudo-foreign key storage (for usage of things like django-ajax-selects)
SINGLE_NUMBER_FIELDS = getattr(settings, "SINGLE_NUMBER_FIELDS", ())

# This is for pseudo-many-to-many key storage
MULTI_NUMBER_FIELDS = getattr(settings, "MULTI_NUMBER_FIELDS", ())
NUMBER_FIELDS = getattr(settings, "CHOICE_FIELDS", ()) + (SINGLE_NUMBER_FIELDS + MULTI_NUMBER_FIELDS)

FIELD_DELIMITER = getattr(settings, "FIELD_DELIMITER", "__")

ADMIN_SORT_JS = getattr(settings, "ADMIN_SORT_JS",
	(
	'https://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
	'scripts/jquery.adminmenusort.js',
	)
)

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])
