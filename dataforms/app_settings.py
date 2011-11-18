"""
Dataforms App Settings
"""

from django.conf import settings

FIELD_MAPPINGS = {}

if hasattr(settings, 'DATAFORMS_FIELD_MAPPINGS'):
	FIELD_MAPPINGS = settings.DATAFORMS_FIELD_MAPPINGS
	
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
	'FileInput' : { 'class': 'django.forms.FileField', 'widget': 'django.forms.ClearableFileInput' },
	'ImageFileInput' : { 'class': 'django.forms.ImageField', 'widget': 'django.forms.ClearableFileInput' },
	'IntegerInput' : { 'class': 'django.forms.IntegerField', 'widget': 'django.forms.TextInput' },
	'DecimalInput' : { 'class': 'django.forms.DecimalField', 'widget': 'django.forms.TextInput' },
	# Note Widget:  This is a way you can add sub headings to your forms.  See - dataforms.widgets.NoteWidget
	'Note' : { 'class': 'django.forms.CharField', 'widget': 'dataforms.widgets.NoteWidget' },
	
	# FIXME: Remove After testing....
	'USStateField' : { 'class': 'django.contrib.localflavor.us.forms.USStateField', 'widget' : 'django.forms.TextInput' },   
} )

# Path for file uploads (don't forget trailing slash)
FILE_UPLOAD_PATH = getattr(settings, "DATAFORMS_FILE_UPLOAD_PATH", "uploads/")

MAX_UPLOAD_SIZE = getattr(settings, "DATAFORMS_MAX_UPLOAD_SIZE", 10485760)

UPLOAD_FIELDS = getattr(settings, "DATAFORMS_UPLOAD_FIELDS", ()) + ('FileInput', 'ImageFileInput')
BOOLEAN_FIELDS = getattr(settings, "DATAFORMS_BOOLEAN_FIELDS", ()) + ('CheckboxInput',)
SINGLE_CHOICE_FIELDS = getattr(settings, "DATAFORMS_SINGLE_CHOICE_FIELDS", ()) + ('Select', 'RadioSelect')
MULTI_CHOICE_FIELDS = getattr(settings, "DATAFORMS_MULTI_CHOICE_FIELDS", ()) + ('SelectMultiple', 'CheckboxSelectMultiple')
# These fields tie into the Choice Model
CHOICE_FIELDS = (SINGLE_CHOICE_FIELDS + MULTI_CHOICE_FIELDS)
# These fields are saved as Comma Delimited Strings (usefull for numbers)
STATIC_CHOICE_FIELDS = getattr(settings, "DATAFORMS_STATIC_CHOICE_FIELDS", ())

FIELD_DELIMITER = getattr(settings, "DATAFORMS_FIELD_DELIMITER", "__")

VALIDATION_MODULE = getattr(settings, "DATAFORMS_VALIDATION_MODULE", "validation")

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])

REMOTE_JQUERY_JS = (
	'https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js',
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js',
)
REMOTE_JQUERY_CSS = (
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/base/jquery-ui.css',
)

ADMIN_JS = REMOTE_JQUERY_JS + (
	'%sdataforms/js/admin.js' % settings.STATIC_URL,
)

FORM_MEDIA = {
	'js' : (
	'%sdataforms/js/ajaxupload.js' % settings.STATIC_URL,
	'%sdataforms/js/bindings.js' % settings.STATIC_URL,
	'%sdataforms/js/datepicker.js' % settings.STATIC_URL,
	),
}

USE_REMOTE_JQUERY = getattr(settings, "DATAFORMS_USE_REMOTE_JQUERY", True)
if USE_REMOTE_JQUERY:
	FORM_MEDIA['js'] = REMOTE_JQUERY_JS + FORM_MEDIA['js']
	FORM_MEDIA['css'] = {
		'all' : REMOTE_JQUERY_CSS
	}
	#FORM_MEDIA['js'].reverse()

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

