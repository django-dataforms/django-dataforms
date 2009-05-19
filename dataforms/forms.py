
# Load the user's custom validation, if it exists
try:
	import validation
except ImportError:
	validation = None

from collections import defaultdict
from django.utils import simplejson as json
from django.utils.datastructures import SortedDict
from django import forms
from settings import FIELD_MAPPINGS
from models import DataForm, DataFormCollection, Field, FieldChoice, Answer

def create_form_collection(slug):
	"""
	Based on a form collection slug, create a list of form objects.
	
	:param slug: the form slug from the DB
	:return: a dictionary containing: ``title``, ``description``, ``slug``, and ``form_list``
	"""
	
	# Get the queryset for the form collection to pass in our dcitionary
	try:
		form_collection_qs = DataFormCollection.objects.get(visible=True,slug=slug)
	except DataFormCollection.DoesNotExist:
		raise Exception('Data From Collection %s does not exist. Make sure the slug name is correct and the collection is visible.' % slug)
	
	# Get queryset for all the forms that are needed
	try:
		forms_qs = (
			DataForm.objects.filter(
				dataformcollectiondataform__data_formcollection__slug=slug,
				dataformcollectiondataform__data_formcollection__visible=True)
			.order_by('dataformcollectiondataform__order')
		)
	except DataForm.DoesNotExist:
		raise Exception('Data Forms for %s do not exist. Make sure the slug name is correct and the forms are visible.' % slug)
	
	# Initialize a list to contain all the form classes
	form_list = []
	
	# Populate the list
	for row in forms_qs:
		form_list.append(_create_form(str(row.slug), title=row.title, description=row.description))
	
	# Pass our collection info and our form list to the dictionary
	form_collection_dict = {
		'title':form_collection_qs.title,
		'description':form_collection_qs.description,
		'slug':form_collection_qs.slug,
		'form_list':form_list,
	}
	
	return form_collection_dict

def create_form(request, slug, title=None, description=None, submission=None):
	"""
	Instantiate and return a dynamic form object.

	:param request: the current page request object, so we can pull POST and other vars.
	:param slug: the form slug from the DB
	:param title: optional title; pulled from DB by default
	:param description: optional description; pulled from DB by default
	:param submission: optional submission; passed in to retieve answers from an existing submittion
	"""
	data = defaultdict(list)
	
	if submission:
		answer_qs = Answer.objects.select_related('field').filter(submission__pk=submission)
		
		for row in answer_qs:
			if row.field.field_type in ('SelectMultiple', 'CheckboxSelectMultiple'):
				data[str(row.field.slug)] += [row.answer,]
			else:
				data[str(row.field.slug)] = row.answer
		
	# Create our form class
	FormClass = _create_form(slug=slug, title=title, description=description)
	
	# Create the instance of our class and pass the POST,FILES if needed
	if request.method == 'POST':
		form = FormClass(request.POST, request.FILES, data if data else None)
	else:
		form = FormClass(data if data else None)
		
	return form

def _create_form(slug, title=None, description=None):
	"""
	Creates a form class object.
	
	:param slug: the form slug in the DB
	:param title: optional title; pulled from DB by default
	:param description: optional description; pulled from DB by default
	"""
	
	meta = {}
	
	# Parse the slug and create a class title
	form_class_title = create_form_class_title(slug)
	
	# Get the queryset detail for the form
	if not title or not description:
		try:
			form_qs = DataForm.objects.get(visible=True,slug=slug)
		except DataForm.DoesNotExist:
			raise Exception('DataForm %s does not exist. Make sure the slug name is correct and the form is visible.' % slug)
		
		# Set the title and/or the description from the DB (but only if it wasn't given)
		meta['title'] = form_qs.title if not title else title
		meta['description'] = form_qs.description if not description else description
		
	# Get all the fields
	try:
		field_qs = Field.objects.filter(dataformfield__data_form__slug=slug,visible=True).order_by('dataformfield__order')
	except Field.DoesNotExist:
		raise Exception('Field for %s do not exist. Make sure the slug name is correct and the fields are visible.' % slug)
		
	# Initialize a sorted dictionary to keep the order of our fields
	fields = SortedDict()
	
	# Finally I figured out the ORM!!  AAAHH!!  So nice to have this outside out loop.
	choices_qs = (
		FieldChoice.objects.select_related('choice', 'field')
			.filter(field__dataformfield__data_form__slug=slug)
			.filter(field__visible=True)
			.order_by('field__dataformfield__order')
	)
	
	#anyone tell you defaultdict is sweet?	
	#we take the data in choices_qs and turn it into a dict so we can reference it later
	choices_dict = defaultdict(tuple)
	
	# Populate our choices dictionary
	for row in choices_qs:
		choices_dict[row.field.pk] += (row.choice.value, row.choice.title),
		
	#populate our fields dictionary
	for row in field_qs:
		kwargs = {}
		
		#TODO: parse any additional arguments in json format and include them in :args:
		if row.arguments:
			json_args = json.loads(row.arguments)
		
		kwargs['label'] = row.label
		kwargs['help_text'] = row.help_text
		kwargs['initial'] = row.initial
		kwargs['required'] = row.required
		
		#fetch the field type mapping from settings.py
		field_type = FIELD_MAPPINGS[row.field_type]
		
		# Add kwargs for ChoiceField and MultipleChoiceField
		if row.field_type in ('Select', 'SelectMultiple', 'CheckboxSelectMultiple', 'RadioSelect'):
			choices = ()

			# We add a separator for select boxes
			if row.field_type == 'Select':
				choices += ('', '--------'),
			
			# Populate our choices tuple
			choices += choices_dict[row.id]
			kwargs['choices'] = choices
			
		#-----Additional logic for field types GO HERE----
		#efif row.field_type == CharField (example)
		
		# Create our field key with any widgets and additional arguments (initial, label, required, help_text, etc)
		fields[row.slug] = field_type['class'](widget=field_type['widget'] if field_type.has_key('widget') else None, **kwargs)
	
	attrs = {
		'base_fields': fields,
		'meta' : meta,
		'slug':slug
	}
	
	# Grab the dynamic validation function from validation.py
	if validation:
		validate = getattr(validation, form_class_title)

		#loop through the functions that exist
		for attr_name in dir(validate):
			#only take functions that start with clean
			if attr_name.startswith('clean'):
				attrs[attr_name] = getattr(validate, attr_name)
	
	# Create a Form class object
	form = type(form_class_title, (forms.BaseForm,), attrs)
	
	return form

def create_form_class_title(slug):
	"""
	Transform "my-form-name" into "MyFormName"
	
	This is important because we need each form class to have a unique name.

	:param slug: the form slug from the DB
	"""

	return ''.join([word.capitalize() for word in slug.split('-')] + ['Form'])



