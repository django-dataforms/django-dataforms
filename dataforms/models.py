from django.db import models
from django.utils.translation import ugettext_lazy as _
from .settings import FIELD_TYPE_CHOICES

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
	section = models.CharField(verbose_name=_('section'), max_length=255, null=False, blank=False)

	class Meta:
		unique_together = ('collection', 'data_form')
		ordering = ['section','order',]

	def __unicode__(self):
		return u'%s in %s' % (self.collection, self.data_form)

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
		ordering = ['order',]
		
	def __unicode__(self):
		return u'%s in %s' % (self.data_form, self.field)
	
class Field(models.Model):
	"""
	Model that holds fields
	"""
	
	choices = models.ManyToManyField('Choice', through='FieldChoice')
	field_type = models.CharField(verbose_name=_('field type key'), max_length=255, choices=FIELD_TYPE_CHOICES)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	label = models.TextField(verbose_name=_('field label'))
	help_text = models.TextField(verbose_name=_('field help text'), blank=True)
	initial = models.TextField(verbose_name=_('initial value of the field'), blank=True)
	arguments = models.CharField(verbose_name=_('additional arguments'), help_text="A JSON dictionary of keyword arguments.", blank=True, max_length=255)
	required = models.BooleanField(verbose_name=_('field is required'), default=False)
	visible = models.BooleanField(verbose_name=_('field is visible'), default=True)
	bindings = models.ManyToManyField('self', symmetrical=False, through="Binding")
	
	def __unicode__(self):
		return self.label

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
		ordering = ['field', 'order',]

	def __unicode__(self):
		return u'%s - %s' % (self.field, str(self.choice).upper())

class Choice(models.Model):
	"""
	Model that holds choices for fields and their values
	"""
	
	title = models.CharField(verbose_name=_('choice title'), max_length=255)
	value = models.CharField(verbose_name=_('choice value'), max_length=255)

	def __unicode__(self):
		return self.title

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
		return str(" - ".join([str(self.answer), self.number]))
	
class Answer(models.Model):
	"""
	Model that holds answers for each submission
	"""
	
	submission = models.ForeignKey('Submission', null=False, blank=False)
	data_form = models.ForeignKey('DataForm', null=False, blank=False)
	field = models.ForeignKey('Field', null=False, blank=False)

	last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)

	def __unicode__(self):
		return str(self.field)
	
	
