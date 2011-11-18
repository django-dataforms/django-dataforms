Dataforms Settings
======================

Below are the available settings for Dataforms that can go in your settings.py file.


``DATAFORMS_FIELD_MAPPINGS``
	A dictionary of form fields are available to be used. The dictionary cat contain
	the following keys:
	
	:class: *required* The full python path to the field class as a string.
	:widget: *required* The full python path to the widget as a string.
	:widget_kwargs: *optional* A dictionary on arguments to pass to the widget.
	:widget_attrs: *optional* A dictionary of widget attrs to pass to the widget.
	
	Here is what is in FIELD_MAPPINGS by default::
	
		{
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
		}
	
``DATAFORMS_FILE_UPLOAD_PATH``
	| A path relative to the MEDIA_ROOT where to store file uploads for Dataforms
	| Be sure to add a trailing shash.
	| *default* = 'uploads/'
	
``DATAFORMS_MAX_UPLOAD_SIZE``
	| The maximum size for an individual file upload in bytes.  This should be a integer.
	| *default* = 10485760

``DATAFORMS_UPLOAD_FIELDS``
	| A tuple of field keys in DATAFORMS_FIELD_MAPPINGS that should be treated as upload fields.
	| *default* = ('FileInput', 'ImageFileInput')

``DATAFORMS_BOOLEAN_FIELDS``
	| A tuple of field keys in DATAFORMS_FIELD_MAPPINGS that should be treated as boolean fields.
	| *default* = ('CheckboxInput',)

``DATAFORMS_SINGLE_CHOICE_FIELDS``
	| A tuple of field keys in DATAFORMS_FIELD_MAPPINGS that should be treated as single choice fields.
	| *default* = ('Select', 'RadioSelect')

``DATAFORMS_MULTI_CHOICE_FIELDS``
	| A tuple of field keys in DATAFORMS_FIELD_MAPPINGS that should be treated as single choice fields.
	| *default* = ('SelectMultiple', 'CheckboxSelectMultiple')

``DATAFORMS_STATIC_CHOICE_FIELDS``
	| A tuple of field keys in DATAFORMS_FIELD_MAPPINGS that should be treated as a comma-delimited string
	| This can be usefull for choice fields that have numbers as their values.
	| *default* = ()

``DATAFORMS_FIELD_DELIMITER``
	| The delimiter to be used in the creation of a field name.
	| *default* = '__'
	
``DATAFORMS_VALIDATION_MODULE``
	| The module path that conains and django form validation that will be used with dataforms.
	| See :doc:`validation` for details.
	| *default* = 'validation'

``DATAFORMS_USE_REMOTE_JQUERY``
	| Specify where or not to use remote JQuery libraries.
	| *default* = True

