from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.conf import settings

FIELD_MAPPINGS = {
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
}

# You need to import your django settings to get the MEDIA_URL for this to work.
ADMIN_SORT_JS = (
	'https://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
	'https://ajax.googleapis.com/ajax/libs/jqueryui/1.7.1/jquery-ui.min.js',
	'%s/scripts/jquery.adminmenusort.js' % settings.MEDIA_URL,
)

FIELD_TYPE_CHOICES = tuple([(field,field) for field in FIELD_MAPPINGS])