from __future__ import absolute_import

# Load the user's custom validation, if it exists
try: import validation
except ImportError: validation = None

# Use cjson if it exists, over Django's simplejson
try: import cjson as json
except ImportError:	from django.utils import simplejson as json

from collections import defaultdict
from django.utils.datastructures import SortedDict
from django import forms
from django.db import transaction
from .settings import FIELD_MAPPINGS, MULTICHOICE_FIELDS
from .models import DataForm, DataFormCollection, Field, FieldChoice, Answer, Submission

class BaseDataForm(forms.BaseForm):
	@transaction.commit_on_success
	def save(self, submission=None, slug=None):
		"""
		Saves the validated, cleaned form data. If a submission already exists,
		the new data will be merged over the old data.
		"""
		
		if not submission:
			if not slug:
				raise RequiredArgument("If no submission is given, a slug must be specified.")
			
			submission = Submission.objects.create(
				slug = slug,
			)
		
#		for key in self.fields.keys():
#			print self.cleaned_data[key]
#			
#			print self.fields[key]
#			print self.fields
#			#if self.fields[key].field_type in ('SelectMultiple', 'CheckboxSelectMultiple'):
#			
#			Answer.objects.create(
#				submission=submission,
#				field=self.fields[key],
#				content=self.cleaned_data[key]
#			)

def create_form_collection(slug):
	"""
	Based on a form collection slug, create a list of form objects.
	
	:param slug: the form slug from the DB
	:return: a dictionary containing: ``title``, ``description``, ``slug``, and ``form_list``
	"""
	
	# Get the queryset for the form collection to pass in our dcitionary
	try:
		form_collection_qs = DataFormCollection.objects.get(visible=True, slug=slug)
	except DataFormCollection.DoesNotExist:
		raise Exception(
			'''DataFormCollection %s does not exist. Make sure the slug
			name is correct and the collection is visible.''' % slug
		)
	
	# Get queryset for all the forms that are needed
	try:
		forms_qs = (
			DataForm.objects.filter(
				dataformcollectiondataform__collection__slug=slug,
				dataformcollectiondataform__collection__visible=True
			).order_by('dataformcollectiondataform__order')
		)
	except DataForm.DoesNotExist:
		raise Exception(
			'''Data Forms for %s do not exist. Make sure the slug
			name is correct and the forms are visible.''' % slug
		)
	
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

def create_form(request, slug, submission=None, title=None, description=None):
	"""
	Instantiate and return a dynamic form object, optionally already populated
	from an already submitted form.

	:param request: the current page request object, so we can pull POST and other vars.
	:param slug: the form slug from the DB
	:param submission: optional submission; passed in to retrieve answers from an existing submission
	:param title: optional title; pulled from DB by default
	:param description: optional description; pulled from DB by default
	"""

	data = defaultdict(list)
	
	if submission:
		answer_qs = Answer.objects.select_related('field', 'choice').filter(submission=submission)
		
		for answer in answer_qs:
			if answer.field.field_type in MULTICHOICE_FIELDS:
				data[str(answer.field.slug)] += [choice.value for choice in answer.choice.all()]
			else:
				data[str(answer.field.slug)] = answer.content
				
	# Create our form class
	FormClass = _create_form(slug=slug, title=title, description=description)
	
	# Create the instance of our class and pass the POST,FILES if needed
	if request.method == 'POST':
		
		# FIXME: `data` here is being sent to the wrong argument (I think you
		# have to merge the data objects over request.POST or find out if
		# Django has a way to do this internally).
		# Why we haven't noticed: Since the form is populated with defaults
		# before the POST has happened, the post-POST form just happens to look
		# like it has been overlayed on top of the DB data.
		
		# On second thought, maybe we don't have to worry about this at all
		# and we can just remove the third argument. Assume that the POST data
		# doesn't need to be merged over the DB data ever. Is there ever a case
		# when POST data will not also contain the DB defaults from the
		# first submission? 
		
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
	
	# Get all the choices associated to fields
	choices_qs = (
		FieldChoice.objects.select_related('choice', 'field')
			.filter(field__dataformfield__data_form__slug=slug)
			.filter(field__visible=True)
			.order_by('field__dataformfield__order')
	)
	
	# Anyone tell you defaultdict is sweet?	
	# We take the data in choices_qs and turn it into a dict so we can reference it later
	choices_dict = defaultdict(tuple)
	
	# Populate our choices dictionary
	for row in choices_qs:
		choices_dict[row.field.pk] += (row.choice.value, row.choice.title),
		
	# Populate our fields dictionary for this form
	for row in field_qs:
		kwargs = {}
		
		# TODO: parse any additional arguments in json format and include them in :args:
		if row.arguments:
			json_args = json.loads(row.arguments)
		
		kwargs['label'] = row.label
		kwargs['help_text'] = row.help_text
		kwargs['initial'] = row.initial
		kwargs['required'] = row.required
		field_type = FIELD_MAPPINGS[row.field_type]
		
		# Add kwargs for ChoiceField and MultipleChoiceField
		
		# FIXME: pull this tuple out to a "constant"
		if row.field_type in ('Select', 'SelectMultiple', 'CheckboxSelectMultiple', 'RadioSelect'):
			choices = ()

			# We add a separator for select boxes
			if row.field_type == 'Select':
				choices += ('', '--------'),
			
			# Populate our choices tuple
			choices += choices_dict[row.id]
			kwargs['choices'] = choices
			
			# If initial has multiple values
			if ',' in kwargs['initial']:
				kwargs['initial'] = kwargs['initial'].split(',')
				
				# remove whitespace
				kwargs['initial'] = [element.strip() for element in kwargs['initial']]
			
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

		# Pull the "clean_" functions from the validation
		# for this form and inject them into the form object
		for attr_name in dir(validate):
			if attr_name.startswith('clean'):
				attrs[attr_name] = getattr(validate, attr_name)
	
	# Return a class object of this form with all attributes
	return type(form_class_title, (BaseDataForm,), attrs)

def create_form_class_title(slug):
	"""
	Transform "my-form-name" into "MyFormName"
	
	This is important because we need each form class to have a unique name.

	:param slug: the form slug from the DB
	"""

	return ''.join([word.capitalize() for word in str(slug).split('-')] + ['Form'])


# Custom dataform exception classes

class RequiredArgument(Exception):
	pass

