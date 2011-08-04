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

if hasattr(settings, 'DATAFORMS_FIELD_MAPPINGS'):
	FIELD_MAPPINGS = settings.FIELD_MAPPINGS
	
FIELD_MAPPINGS.update( {
	'TextInput' : { 'class': 'django.forms.CharField', 'widget': 'django.forms.TextInput' },
	'Textarea' : { 'class': 'django.forms.CharField', 'widget': 'django.forms.Textarea' },
	'Select' : { 'class': 'django.forms.ChoiceField', 'widget': 'django.forms.Select' },
	'SelectMultiple' : { 'class': 'django.forms.MultipleChoiceField', 'widget': 'django.forms.SelectMultiple' },
	'RadioSelect' : { 'class': 'django.forms.ChoiceField', 'widget': 'django.forms.RadioSelect' },
	'Password' : { 'class': 'django.forms.CharField', 'widget': 'django.forms.PasswordInput', 'widget_kwargs' : { 'render_value' : True } },
	'Email' : { 'class': 'django.forms.EmailField', 'widget': 'django.forms.TextInput' },
	'DateField' : { 'class': 'django.forms.DateField', 'widget': 'django.forms.DateTimeInput', 'widget_attrs' : { 'class' : 'datepicker' } },
	'CheckboxInput' : { 'class': 'django.forms.BooleanField', 'widget': 'django.forms.CheckboxInput' },
	'CheckboxSelectMultiple': { 'class': 'django.forms.MultipleChoiceField', 'widget': 'django.forms.CheckboxSelectMultiple' },
	'HiddenInput' : { 'class': 'django.forms.Field', 'widget': 'django.forms.HiddenInput' },
	'FileInput' : { 'class': 'django.forms.FileField', 'widget': 'dataforms.widgets.FileWidget' },
	'IntegerInput' : { 'class': 'django.forms.IntegerField', 'widget': 'django.forms.TextInput' },
	# Note Widget:  This is a way you can add sub headings to your forms.  See - dataforms.widgets.NoteWidget
	'Note' : { 'class': 'django.forms.CharField', 'widget': 'dataforms.widgets.NoteWidget' },
	
	
	
	# FIXME: Remove After testing....
	'USStateField' : { 'class': 'django.contrib.localflavor.us.forms.USStateField', 'widget' : 'django.forms.TextInput' },   
} )

MAX_UPLOAD_SIZE = getattr(settings, "DATAFORMS_MAX_UPLOAD_SIZE", 10485760)

UPLOAD_FIELDS = getattr(settings, "DATAFORMS_UPLOAD_FIELDS", ()) + ('FileInput','AjaxSingleFileUpload',)
BOOLEAN_FIELDS = getattr(settings, "DATAFORMS_BOOLEAN_FIELDS", ()) + ('CheckboxInput',)
SINGLE_CHOICE_FIELDS = getattr(settings, "DATAFORMS_SINGLE_CHOICE_FIELDS", ()) + ('Select', 'RadioSelect')
MULTI_CHOICE_FIELDS = getattr(settings, "DATAFORMS_MULTI_CHOICE_FIELDS", ()) + ('SelectMultiple', 'CheckboxSelectMultiple')
# These fields tie into the Choice Model
CHOICE_FIELDS = getattr(settings, "DATAFORMS_CHOICE_FIELDS", ()) + (SINGLE_CHOICE_FIELDS + MULTI_CHOICE_FIELDS)
# These fields are saved as Comma Delimited Strings (usefull for numbers)
STATIC_CHOICE_FIELDS = getattr(settings, "DATAFORMS_STATIC_CHOICE_FIELDS", ())

FIELD_DELIMITER = getattr(settings, "DATAFORMS_FIELD_DELIMITER", "__")

VALIDATION_MODULE = getattr(settings, "DATAFORMS_VALIDATION_MODULE", "validation")

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])

ADMIN_SORT_JS = (
	'https://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
	'%sdataforms/js/jquery.adminmenusort.js' % settings.STATIC_URL,
)

FORM_MEDIA = {
	'js' : [
	'%sdataforms/js/ajaxupload.js' % settings.STATIC_URL,
	'%sdataforms/js/bindings.js' % settings.STATIC_URL,
	'%sdataforms/js/datepicker.js' % settings.STATIC_URL,
	],
}

USE_REMOTE_JQUERY = getattr(settings, "USE_REMOTE_JQUERY", True)
if USE_REMOTE_JQUERY:
	FORM_MEDIA['js'].extend([
		'http://code.jquery.com/ui/1.8.14/jquery-ui.min.js',
		'http://code.jquery.com/jquery.min.js',
	])
	FORM_MEDIA['css'] = {
		'all' : ('http://code.jquery.com/ui/1.8.14/themes/base/jquery-ui.css',)
	}
	FORM_MEDIA['js'].reverse()

BINDING_OPERATOR_CHOICES = (
    ('checked', 'Checked or Has Value',),
    ('equal', 'Equal',),
    ('not-equal', 'Not Equal',),
    ('contain', 'Contains',),
    ("not-contain", "Doesn't Contain",),
)

BINDING_ACTION_CHOICES = (
    ('show-hide', 'Show/Hide',),
    ('function', 'Custom Function',),
)

