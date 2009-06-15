"""
Forms System
============
"""

# Load the user's custom validation, if it exists
try: import validation
except ImportError: validation = None

from collections import defaultdict
from django import forms
from django.db import transaction
from django.utils import simplejson as json
from django.utils.datastructures import SortedDict

from .settings import FIELD_MAPPINGS, SINGLE_CHOICE_FIELDS, MULTI_CHOICE_FIELDS, CHOICE_FIELDS, BOOLEAN_FIELDS, FIELD_DELIMITER
from .models import DataForm, Collection, Field, FieldChoice, Choice, Answer, Submission, AnswerChoice

class BaseDataForm(forms.BaseForm):
	@transaction.commit_on_success
	def save(self):
		"""
		Saves the validated, cleaned form data. If a submission already exists,
		the new data will be merged over the old data.
		"""
		
		# TODO: think about adding an "overwrite" argument to this function, default of False,
		# which will determine if an error should be thrown if the submission object already
		# exists, or if we should trust the data and overwrite the previous submission.

		# FIXME: This is probably ridiculously inefficient and may generate a ton of SQL.
		# Do some profiling and see if there are ways to batch some of the SQL queries together.
		#
		# Specifically:
		#  * All the get_or_create() functions could become creates if we delete all answers
		#    that we are about to update.
		#  * Is there any way to batch INSERTs in Django's ORM?
		
		if not hasattr(self, "submission"):
			# This needs to be get_or_create (not just create) for form collections
			# IE, the first form saved in a collection will create the submission
			# but all other forms will still not have self.submission
			self.submission, was_created = Submission.objects.get_or_create(slug=self.submission_slug)
		
		for key in self.fields.keys():
			# Mangle the key into the DB form, then get the right Field
			field = Field.objects.get(slug=_field_for_db(key))
			
			if field.field_type in CHOICE_FIELDS:
				# This is an answer that is tied to the choices relation, not content
				
				answer, was_created = Answer.objects.get_or_create(
					submission=self.submission,
					field=field,
					data_form=DataForm.objects.get(slug=self.slug),
				)
				
				# Delete all previous choices
				answer.choices.clear()
				
				# If string, wrap as a list because the for-loop below assumes a list
				if isinstance(self.cleaned_data[key], unicode) or isinstance(self.cleaned_data[key], str):
					self.cleaned_data[key] = [self.cleaned_data[key]]
				
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
					data_form=DataForm.objects.get(slug=self.slug),
				)
				
				# Update the content and re-save.
				answer.content = content=self.cleaned_data[key] if self.cleaned_data[key] else ''
				answer.save()

class BaseCollection(object):
	def __init__(self, title, description, slug, forms):
		self.title = str(title)
		self.description = str(description)
		self.slug = str(slug)
		self.forms = forms
		
	def __getitem__(self, index):
		return self.forms[index]
	
	def __getslice__(self, start, end):
		return self.forms[start, end]
	
	# FIXME: does this transaction encapsulate the inner save()
	# transactions? If not, we need to do that.
	@transaction.commit_on_success
	def save(self):
		"""
		Save all contained forms
		"""
		
		for form in self.forms:
			form.save()
		
	def is_valid(self):
		"""
		Validate all contained forms
		"""
		
		for form in self.forms:
			if not form.is_valid():
				return False
		return True

def create_collection(request, collection, submission):
	"""
	Based on a form collection slug, create a list of form objects.
	
	:param request: the current page request object, so we can pull POST and other vars.
	:param collection: a data form collection slug or object
	:param submission: create-on-use submission slug or object; passed in to retrieve
		Answers from an existing Submission, or to be the slug for a new Submission.
	:return: a BaseCollection object, populated with the correct data forms and data
	"""
	
	# Slightly evil, do type checking to see if submission is a Submission object or string
	if isinstance(collection, str):
		# Get the queryset for the form collection to pass in our dictionary
		try:
			form_collection_qs = Collection.objects.get(visible=True, slug=collection)
		except Collection.DoesNotExist:
			raise Collection.DoesNotExist('''Collection %s does not exist. Make sure the slug name is correct and the collection is visible.''' % collection)
	
	# Get queryset for all the forms that are needed
	try:
		forms_qs = DataForm.objects.filter(
				collectiondataform__collection__slug=collection,
				collectiondataform__collection__visible=True
			).order_by('collectiondataform__order')
	except DataForm.DoesNotExist:
		raise DataForm.DoesNotExist('''Data Forms for collection %s	do not exist. Make sure the slug name is correct and the forms are visible.''' % collection)
	
	# Initialize a list to contain all the form classes
	form_list = []
	
	# Populate the list
	for form in forms_qs:
		form_list.append(create_form(request, form=form, submission=submission))
	
	# Pass our collection info and our form list to the dictionary
	collection = BaseCollection(
		title=form_collection_qs.title,
		description=form_collection_qs.description,
		slug=form_collection_qs.slug,
		forms=form_list
	)
	
	return collection

def create_form(request, form, submission, title=None, description=None):
	"""
	Instantiate and return a dynamic form object, optionally already populated from an
	already submitted form.
	
	Usage::
	
		# Get a dynamic form. If a Submission with slug "myForm" exists,
		# this will return a bound form. Otherwise, it will be unbound.
		create_form(request, form="personal-info", submission="myForm")
		
		# Create a bound form to a previous submission object
		create_form(request, slug="personal-info", submission=Submission.objects.get(...))

	:param request: the current page request object, so we can pull POST and other vars.
	:param form: a data form slug or object
	:param submission: create-on-use submission slug or object; passed in to retrieve
		Answers from an existing Submission, or to be the slug for a new Submission.
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
	
	# Make sure the form definition exists before continuing
	try:
		form_qs = DataForm.objects.get(visible=True, slug=slug)
	except DataForm.DoesNotExist:
		raise DataForm.DoesNotExist('DataForm %s does not exist. Make sure the slug name is correct and the form is visible.' % slug)
	
	# Get the queryset detail for the form
	if not title or not description:
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
		# FIXME: is this error ever going to be raised? Won't it just be [] and not raise an error?
		raise Field.DoesNotExist('Field for %s do not exist. Make sure the slug name is correct and the fields are visible.' % slug)
		
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
		fields[_field_for_form(name=row.slug, form=slug)] = field_type['class'](widget=field_type['widget'] if field_type.has_key('widget') else None, **kwargs)
	
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

def get_answers(submission):
	"""
	Get the answers for a submission
	
	:return: a dictionary of answers
	"""
	
	data = defaultdict(list)
	
	answer_qs = Answer.objects.select_related('field', 'choice').filter(submission=submission)
		
	# For every answer, 
	for answer in answer_qs:
		
		# Refactor the answer field name to be globally unique (so
		# that a field can be in multiple forms in the same POST)
		answer_key = _field_for_form(name=str(answer.field.slug), form=answer.data_form.slug) 
		
		if answer.field.field_type in MULTI_CHOICE_FIELDS:
			data[answer_key] += [choice.value for choice in answer.choices.all()]
		elif answer.field.field_type in SINGLE_CHOICE_FIELDS:
			try:
				data[answer_key] = [choice.value for choice in answer.choices.all()][0]
			except IndexError:
				# If we couldn't find a choice relation, just use the DB default
				pass
		else:
			data[answer_key] = answer.content
			
	return dict(data)

def create_form_class_title(slug):
	"""
	Transform "my-form-name" into "MyFormName"
	This is important because we need each form class to have a unique name.

	:param slug: the form slug from the DB
	"""

	return ''.join([word.capitalize() for word in str(slug).split('-')] + ['Form'])

def _field_for_form(name, form):
	"""
	Make a form field globally unique by prepending the form name
	field-name --> form-name--field-name
	"""
	return "%s%s%s" % (form, FIELD_DELIMITER, name)

def _field_for_db(name):
	"""
	Take a form from POST data and get it back to its DB-capable name
	id_form-name--field-name --> field-name 
	"""
	return name[name.find(FIELD_DELIMITER)+len(FIELD_DELIMITER):]

# Custom dataform exception classes
class RequiredArgument(Exception):
	pass

