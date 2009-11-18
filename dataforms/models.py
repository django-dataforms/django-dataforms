from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from .settings import FIELD_TYPE_CHOICES
from itertools import izip
from collections import defaultdict

class Collection(models.Model):
	"""
	Model that holds a collection of forms
	"""

	data_forms = models.ManyToManyField('DataForm', through='CollectionDataForm')
	title = models.CharField(verbose_name=_('collection title'), max_length=255)
	description = models.TextField(verbose_name=_('description'), blank=True)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	visible = models.BooleanField(verbose_name=_('collection is visible'), default=True)

	def __unicode__(self):
		return self.title

class CollectionDataForm(models.Model):
	""" 
	Model bridge for Collection and DataForm
	"""

	collection = models.ForeignKey('Collection', null=True)
	data_form = models.ForeignKey('DataForm', null=True)
	order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)
	section = models.ForeignKey('Section', null=True)

	class Meta:
		unique_together = ('collection', 'data_form')
		ordering = ['order',]

	def __unicode__(self):
		return u'%s in %s' % (self.collection, self.data_form)

class Section(models.Model):
	"""
	Model that gives a section to a DataForm within a Collection
	"""
	title = models.CharField(verbose_name=_('section'), max_length=255, null=False, blank=False)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)

	def __unicode__(self):
		return self.title

class DataForm(models.Model):
	"""
	Model for each form
	"""

	fields = models.ManyToManyField('Field', through='DataFormField')
	title = models.CharField(verbose_name=_('form title'), max_length=255)
	description = models.TextField(verbose_name=_('description'), blank=True)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	visible = models.BooleanField(verbose_name=_('form is visible'), default=True)

	def __unicode__(self):
		return self.title

class DataFormField(models.Model):
	""" 
	Model bridge for DataForm and Field
	"""

	data_form = models.ForeignKey('DataForm', null=True)
	field = models.ForeignKey('Field', null=True)
	order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

	class Meta:
		unique_together = ('data_form', 'field')
		ordering = ['order', ]

	def __unicode__(self):
		return u'%s in %s' % (self.data_form, self.field)

class Field(models.Model):
	"""
	Model that holds fields
	"""

	choices = models.ManyToManyField('Choice', through='FieldChoice')
	field_type = models.CharField(verbose_name=_('field type key'), max_length=255, choices=FIELD_TYPE_CHOICES)
	label = models.TextField(verbose_name=_('field label'))
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	help_text = models.TextField(verbose_name=_('field help text'), blank=True)
	initial = models.TextField(verbose_name=_('initial value of the field'), blank=True)
	arguments = models.CharField(verbose_name=_('additional arguments'), help_text="A JSON dictionary of keyword arguments.", blank=True, max_length=255)
	required = models.BooleanField(verbose_name=_('field is required'), default=False)
	visible = models.BooleanField(verbose_name=_('field is visible'), default=True)

	def __unicode__(self):
		return self.slug

class Binding(models.Model):
	data_form = models.ForeignKey('DataForm', null=False, blank=False)
	parent_fields = models.ManyToManyField('Field', related_name='fields_set', through='ParentField')
	parent_choices = models.ManyToManyField('FieldChoice', related_name='choices_set', through='ParentFieldChoice')
	children = models.ManyToManyField('Field', through='ChildField')

class ParentField(models.Model):
	binding = models.ForeignKey('Binding')
	parent_field = models.ForeignKey('Field', help_text="Leave blank if a choice is selected", null=False, blank=False)
	
class ParentFieldChoice(models.Model):
	binding = models.ForeignKey('Binding')
	field_choice = models.ForeignKey('FieldChoice', help_text="Leave blank if a parent is selected", null=False, blank=False)
	
class ChildField(models.Model):
	binding = models.ForeignKey('Binding')
	field = models.ForeignKey('Field', null=False, blank=False)

class FieldChoice(models.Model):
	""" 
	Model bridge for Field and Choice
	"""

	# FIXME: Why are these nullable?
	field = models.ForeignKey('Field', null=True)
	choice = models.ForeignKey('Choice', null=True)
	order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

	class Meta:
		unique_together = ('field', 'choice')
		ordering = ['field', 'order', ]

	def __unicode__(self):
		return u'%s - %s' % (self.field, unicode(self.choice).upper())

class Choice(models.Model):
	"""
	Model that holds choices for fields and their values
	"""

	title = models.CharField(verbose_name=_('choice title'), max_length=255)
	value = models.CharField(verbose_name=_('choice value'), max_length=255)

	def __unicode__(self):
		return unicode(self.title)

class Submission(models.Model):
	"""
	Model that holds a unique submission
	"""

	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	collection = models.ForeignKey('Collection', null=True, blank=True)
	last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)

	def __unicode__(self):
		return unicode(self.slug)

class AnswerChoice(models.Model):
	"""
	Stores the data for an answer that is a choice
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	choice = models.ForeignKey('Choice', null=False, blank=False)

	def __unicode__(self):
		return unicode(" - ".join([unicode(self.answer), unicode(self.choice)]))

class AnswerText(models.Model):
	"""
	Stores the data for an answer that text
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	text = models.TextField(verbose_name=_('content'), null=False, blank=False)

	def __unicode__(self):
		return unicode(" - ".join([unicode(self.answer), unicode(self.text)]))

class AnswerNumber(models.Model):
	"""
	Stores the data for an answer that text
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	
	# This used to be named "number", but that breaks when using an Oracle
	# database backend because "number" is a reserved word.
	# http://code.djangoproject.com/ticket/4140
	num = models.IntegerField(verbose_name=_('num'), null=False, blank=False)

	def __unicode__(self):
		return unicode(" - ".join([unicode(self.answer), unicode(self.num)]))

class AnswerManager(models.Manager):
	"""(Protocol manager description)"""
	def get_answer_data(self, submission, field_slug=None):

		data = {}
		cursor = connection.cursor()
		qkeys = ['id', 'dataform_slug', 'field_slug', 'field_type', 'choice_value', 'num', 'text']
		query = ["""
			SELECT a.id, df.slug AS dataform_slug, f.slug AS field_slug, f.field_type, c.value AS choice_value, an.num, at.text
			FROM dataforms_answer a
				INNER JOIN dataforms_field f ON (a.field_id = f.id)
				INNER JOIN dataforms_dataform df ON (a.data_form_id = df.id)
				LEFT JOIN dataforms_answerchoice ac ON (a.id = ac.answer_id)
				LEFT JOIN dataforms_choice c ON (ac.choice_id = c.id)
				LEFT JOIN dataforms_answernumber an ON (a.id = an.answer_id)
				LEFT JOIN dataforms_answertext at ON (a.id = at.answer_id)
			WHERE a.submission_id = %s
		"""]
		args = [submission]
		
		if field_slug is not None:
			query.append(" AND f.slug = %s")
			args.append(field_slug)
		
		cursor.execute("".join(query), args)
		
		row = cursor.fetchone()
		while row is not None:
			key = hash(row[:3])
			if not data.has_key(key):
				data[key] = dict(izip(qkeys, row))
				data[key]['content'] = []
			
			# Get the last three of the query ['choice_value', 'num', 'text']
			content_items = row[4:]
			
			# Because of the LEFT JOIN, two of the three will be None.
			# Choose the one that has content, or return None.
			inner_item = (
				# Choice value
				content_items[0] if content_items[0]
				# Number
				else content_items[1] if content_items[1]
				# Text (forced to evaluate for Oracle LOB objects via unicode())
				else unicode(content_items[2]) if content_items[2] is not None
				else None
			)
			data[key]['content'].append(inner_item)
			
			# Fetch a new row
			row = cursor.fetchone()

		return data.values()

class Answer(models.Model):
	"""
	Model that holds answers for each submission
	"""

	submission = models.ForeignKey('Submission', null=False, blank=False)
	data_form = models.ForeignKey('DataForm', null=False, blank=False)
	field = models.ForeignKey('Field', null=False, blank=False)

	def __unicode__(self):
		return unicode(self.field)

	objects = AnswerManager()
