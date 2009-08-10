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
	bindings = models.ManyToManyField('self', symmetrical=False, through="Binding")

	def __unicode__(self):
		return "%s (%s)" % (self.label, self.slug)

class Binding(models.Model):
	"""
	Recursive model bridge for Field
	"""

	data_form = models.ForeignKey('DataForm', null=False, blank=False)
	parent_field = models.ForeignKey('Field', related_name="bindingparent_set", help_text="Leave blank if a choice is selected", null=True, blank=True)
	parent_choice = models.ForeignKey('FieldChoice', help_text="Leave blank if a parent is selected", null=True, blank=True)
	child = models.ForeignKey('Field', related_name="bindingchild_set", null=False, blank=False)

class FieldChoice(models.Model):
	""" 
	Model bridge for Field and Choice
	"""

	field = models.ForeignKey('Field', null=True)
	choice = models.ForeignKey('Choice', null=True)
	order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

	class Meta:
		unique_together = ('field', 'choice')
		ordering = ['field', 'order', ]

	def __unicode__(self):
		return u'%s - %s' % (self.field, str(self.choice).upper())

class Choice(models.Model):
	"""
	Model that holds choices for fields and their values
	"""

	title = models.CharField(verbose_name=_('choice title'), max_length=255)
	value = models.CharField(verbose_name=_('choice value'), max_length=255)

	def __unicode__(self):
		return str(self.title)

class Submission(models.Model):
	"""
	Model that holds a unique submission
	"""

	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	collection = models.ForeignKey('Collection', null=True, blank=True)
	last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)

	def __unicode__(self):
		return '%s' % (self.slug)

class AnswerChoice(models.Model):
	"""
	Stores the data for an answer that is a choice
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	choice = models.ForeignKey('Choice', null=False, blank=False)

	def __unicode__(self):
		return str(" - ".join([str(self.answer), str(self.choice)]))

class AnswerText(models.Model):
	"""
	Stores the data for an answer that text
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	text = models.TextField(verbose_name=_('content'), null=False, blank=False)

	def __unicode__(self):
		return str(" - ".join([str(self.answer), self.text]))

class AnswerNumber(models.Model):
	"""
	Stores the data for an answer that text
	"""
	answer = models.ForeignKey('Answer', null=False, blank=False)
	number = models.IntegerField(verbose_name=_('number'), null=False, blank=False)

	def __unicode__(self):
		return str(" - ".join([str(self.answer), str(self.number)]))

class AnswerManager(models.Manager):
	"""(Protocol manager description)"""
	def get_answer_data(self, submission):

		cursor = connection.cursor()
		query = """
			SELECT a.id, df.slug AS dataform_slug, f.slug AS field_slug, f.field_type, c.value AS choice_value, an.number, at.text
			FROM dataforms_answer AS a 
				INNER JOIN dataforms_field AS f ON (a.field_id = f.id)
				INNER JOIN dataforms_dataform AS df ON (a.data_form_id = df.id)
				LEFT JOIN dataforms_answerchoice AS ac ON (a.id = ac.answer_id)
					LEFT JOIN dataforms_choice AS c ON (ac.choice_id = c.id)
				LEFT JOIN dataforms_answernumber AS an ON (a.id = an.answer_id)
				LEFT JOIN dataforms_answertext AS at ON (a.id = at.answer_id)
			WHERE a.submission_id = %s
			
		"""
		cursor.execute(query, [submission])

		# Make sure this stays in sync with the above query columns
		qkeys = ['id', 'dataform_slug', 'field_slug', 'field_type', 'choice_value', 'number', 'text']
		rows = cursor.fetchall()

		data = {}

		for row in rows:
			key = hash(row[:3])
			if not data.has_key(key):
				data[key] = dict(izip(qkeys, row))
				data[key]['content'] = []

			content_items = row[4:]
			inner_item = (content_items[0] if content_items[0] else content_items[1] if content_items[1] else content_items[2])
			data[key]['content'].append(inner_item)

		return data.values()

class Answer(models.Model):
	"""
	Model that holds answers for each submission
	"""

	submission = models.ForeignKey('Submission', null=False, blank=False)
	data_form = models.ForeignKey('DataForm', null=False, blank=False)
	field = models.ForeignKey('Field', null=False, blank=False)

	def __unicode__(self):
		return str(self.field)

	objects = AnswerManager()

