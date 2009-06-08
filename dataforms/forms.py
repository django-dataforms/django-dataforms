from __future__ import absolute_import

# Load the user's custom validation, if it exists
try: import validation
except ImportError: validation = None

from django import forms
from django.db import transaction
from django.utils import simplejson as json
from django.utils.datastructures import SortedDict

from collections import defaultdict
from .settings import FIELD_MAPPINGS, SINGLE_CHOICE_FIELDS, MULTI_CHOICE_FIELDS, CHOICE_FIELDS, BOOLEAN_FIELDS
from .models import DataForm, DataFormCollection, Field, FieldChoice, Choice, Answer, Submission, AnswerChoice

class BaseDataForm(forms.BaseForm):
	@transaction.commit_on_success
	def save(self):
		"""
		Saves the validated, cleaned form data. If a submission already exists,
		the new data will be merged over the old data.
		"""

		if not hasattr(self, "submission"):
			self.submission = Submission.objects.create(slug=self.submission_slug)
			
		# Make sure that this submission has at least my (self) DataForm associated with
		# it which it needs in order to save properly
		self.submission.data_forms.add(DataForm.objects.get(slug=self.slug))
		
		# FIXME: This is probably ridiculously inefficient and may generate a ton of SQL.
		# Do some profiling and see if there are ways to batch some of the SQL queries together.
		#
		# Specifically:
		#  * All the get_or_create() functions could become creates if we delete all answers
		#    that we are about to update.
		#  * Is there any way to batch INSERTs in Django's ORM?
		
		for key in self.fields.keys():
			field = Field.objects.get(slug=key)
			
			if field.field_type in CHOICE_FIELDS:
				# This is an answer that is tied to the choices relation, not content
				
				answer, was_created = Answer.objects.get_or_create(
					submission=self.submission,
					field=field,
				)
				
				# If string, wrap as a list because the for-loop below assumes a list
				if isinstance(self.cleaned_data[key], unicode) or isinstance(self.cleaned_data[key], str):
					self.cleaned_data[key] = [self.cleaned_data[key]]
				
				# Delete all previous choices
				answer.choices.clear()
				
				# Add the selected choices
				choices = Choice.objects.filter(value__in=self.cleaned_data[key])
				for choice in choices:
					AnswerChoice.objects.get_or_create(
						choice=choice,
						answer=answer
					)
			else:
				# Single answer with content, no choice relations needed
				answer, was_created = Answer.objects.get_or_create(
					submission=self.submission,
					field=field,
				)
				
				# Update the content and re-save.
				answer.content = content=self.cleaned_data[key] if self.cleaned_data[key] else ''
				answer.save()

def create_form_collection(slug):
	"""
	Based on a form collection slug, create a list of form objects.
	
	:param slug: the form slug from the DB
	:return: a dictionary containing: ``title``, ``description``, ``slug``, and ``form_list``
	"""
	
	# Get the queryset for the form collection to pass in our dictionary
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

def get_answers(submission):
	"""
	Get the answers for a submission
	
	:return: a dictionary of answers
	"""
	
	data = defaultdict(list)
	
	answer_qs = Answer.objects.select_related('field', 'choice').filter(submission=submission)
		
	for answer in answer_qs:
		if answer.field.field_type in MULTI_CHOICE_FIELDS:
			data[str(answer.field.slug)] += [choice.value for choice in answer.choices.all()]
		elif answer.field.field_type in SINGLE_CHOICE_FIELDS:
			try:
				data[str(answer.field.slug)] = [choice.value for choice in answer.choices.all()][0]
			except IndexError:
				# If we couldn't find a choice relation, just use the DB default
				pass
		else:
			data[str(answer.field.slug)] = answer.content
			
	return dict(data)

def create_form(request, form, submission=None, title=None, description=None):
	"""
	Instantiate and return a dynamic form object, optionally already populated from an
	already submitted form.
	
	Either called to create an unbound form::
	
		create_form(request, slug="personal-info")
		# or
		create_form(request, slug="personal-info", title="Title", description="Desc")
		
	or to create a bound form tied to a previous submission::
	
		create_form(request, slug="personal-info", submission=Submission.objects.get(...))

	:param request: the current page request object, so we can pull POST and other vars.
	:param form: a data form slug or object
	:param submission: submission slug or object;passed in to retrieve answers from an existing submission
	:param title: optional title; pulled from DB by default
	:param description: optional description; pulled from DB by default
	"""
	
	data = None

	# Slightly evil, do type checking to see if submission is a Submission object or string
	if isinstance(submission, str):
		submission_slug = submission
		
		try:
			submission = Submission.objects.get(slug=submission)
		except Submission.DoesNotExist:
			submission = None
	else:
		submission_slug = submission.slug
		
	# Before we populate from submitted data, prepare the answers for insertion into the form
	if submission:
		data = get_answers(submission=submission)
	
	# Create our form class
	FormClass = _create_form(form=form, title=title, description=description)
	
	# Create the actual form instance, from the dynamic form class
	if request.method == 'POST':
		# We assume here that we don't need to overlay the POST data on top of the database
		# data because the initial form, before POST, will contain the database defaults and so
		# the resulting POST data will (in normal cases) originate from database defaults already.
		
		# This creates a bound form object.
		
		form = FormClass(data=request.POST, files=request.FILES)
	else:
		# We populate the initial data of the form from the database answers. Any questions we
		# don't have answers for in the database will use their initial field defaults.
		
		# This creates an unbound form object.
		form = FormClass(initial=(data if data else None))
		
	# Now that we have an instantiated form object, let's add our custom attributes
	if submission:
		form.submission = submission
	if submission_slug:
		form.submission_slug = submission_slug
		
	return form

def _create_form(form, title=None, description=None):
	"""
	Creates a form class object.

	Usage::
	
		FormClass = _create_form(dataform="myForm")
		form = FormClass(data=request.POST)
	
	:param form: a data form slug or object
	:param title: optional title; pulled from DB by default
	:param description: optional description; pulled from DB by default
	"""
	
	meta = {}
	slug = form if isinstance(form, str) else form.slug
	
	# Parse the slug and create a class title
	form_class_title = create_form_class_title(slug)
	
	# Get the queryset detail for the form
	if not title or not description:
		try:
			form_qs = DataForm.objects.get(visible=True, slug=slug)
		except DataForm.DoesNotExist:
			raise Exception('DataForm %s does not exist. Make sure the slug name is correct and the form is visible.' % slug)
		
		# Set the title and/or the description from the DB (but only if it wasn't given)
		meta['title'] = form_qs.title if not title else title
		meta['description'] = form_qs.description if not description else description
		
	# Get all the fields
	try:
		field_qs = Field.objects.filter(
			dataformfield__data_form__slug=slug,
			visible=True
		).order_by('dataformfield__order')
	except Field.DoesNotExist:
		raise Exception('Field for %s do not exist. Make sure the slug name is correct and the fields are visible.' % slug)
		
	# Initialize a sorted dictionary to keep the order of our fields
	fields = SortedDict()
	
	# Get all the choices associated to fields
	choices_qs = (
		FieldChoice.objects.select_related('choice', 'field').filter(
			field__dataformfield__data_form__slug=slug,
			field__visible=True
		)
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
		
		# Get the choices for single and multiple choice fields 
		if row.field_type in CHOICE_FIELDS:
			choices = ()

			# We add a separator for select boxes
			if row.field_type == 'Select':
				choices += ('', '--------'),
			
			# Populate our choices tuple
			choices += choices_dict[row.id]
			kwargs['choices'] = choices
			
			if row.field_type in MULTI_CHOICE_FIELDS:
				# Get all of the specified default selected values (as a list, even if one element)
				kwargs['initial'] = kwargs['initial'].split(',') if ',' in kwargs['initial'] else [kwargs['initial'],]
				# Remove whitespace so the user can use spaces
				kwargs['initial'] = [element.strip() for element in kwargs['initial']]
			
		#-----Additional logic for field types GO HERE----
		#efif row.field_type == CharField (example)
		
		# Create our field key with any widgets and additional arguments (initial, label, required, help_text, etc)
		fields[row.slug] = field_type['class'](widget=field_type['widget'] if field_type.has_key('widget') else None, **kwargs)
	
	attrs = {
		'base_fields' : fields,
		'meta' : meta,
		'slug' : slug,
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

