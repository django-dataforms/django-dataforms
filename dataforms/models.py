from django.db import models
from django.utils.translation import ugettext_lazy as _
from settings import FIELD_TYPE_CHOICES


class DataFormCollection(models.Model):
	"""
	Model that holds a collection of forms
	"""
	
	data_forms = models.ManyToManyField('DataForm', through='DataFormCollectionDataForm')
	title = models.CharField(verbose_name=_('collection title'), max_length=255)
	description = models.TextField(verbose_name=_('description'), blank=True)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	visible = models.BooleanField(verbose_name=_('collection is visible'), default=True)
	
	def __unicode__(self):
		return self.title

class DataFormCollectionDataForm(models.Model):
	""" 
	Model bridge for DataFormset and DataForm
	"""
	
	collection = models.ForeignKey('DataFormCollection', null=True)
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
	field_type = models.CharField(verbose_name=_('feild type key'), max_length=255, choices=FIELD_TYPE_CHOICES)
	slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
	label = models.TextField(verbose_name=_('field label'))
	help_text = models.TextField(verbose_name=_('field help text'), blank=True)
	initial = models.TextField(verbose_name=_('initial value of the field'), blank=True)
	arguments = models.CharField(verbose_name=_('additional arguments'), blank=True, max_length=255)
	required = models.BooleanField(verbose_name=_('field is required'), default=False)
	visible = models.BooleanField(verbose_name=_('field is visible'), default=True)
	
	def __unicode__(self):
		return self.label

	# def __unicode__(self):
	# 	field_dict = {}
	# 	for d in self.__dict__:
	# 		field_dict[d] = eval('self.%s' % d)
	# 	return unicode(field_dict)

class FieldChoice(models.Model):
	""" 
	Model bridge for Field and Choice
	"""
	
	field = models.ForeignKey('Field', null=True)
	choice = models.ForeignKey('Choice', null=True)
	order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

	class Meta:
		unique_together = ('field', 'choice')
		ordering = ['order',]

	def __unicode__(self):
		return u'%s in %s' % (self.field, self.choice)


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
	# TODO: I don't think we need a relation between a submission to a data collection
	# collection = models.ForeignKey('DataFormCollection', null=True, blank=True)
	
	# FIXME: find a way to make at least one m2m data_forms relation required 
	data_forms = models.ManyToManyField('DataForm', null=False, blank=False)
	last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)

	def __unicode__(self):
		return '%s-%s' % (self.slug, self.pk)


class AnswerChoice(models.Model):
	"""
	Model that bridges choices for answers in a submission
	"""
	
	# Right now, we don't need extra fields here, but we need this
	# m2m model to be present so we can reference it in the view
	
	answer = models.ForeignKey('Answer', null=False, blank=False)
	choice = models.ForeignKey('Choice', null=False, blank=False)
	
class Answer(models.Model):
	"""
	Model that holds answers for each submission
	"""
	
	choices = models.ManyToManyField('Choice', through='AnswerChoice')
	submission = models.ForeignKey('Submission')
	field = models.ForeignKey('Field')
	content = models.TextField(verbose_name=_('content'), null=True, blank=True)
	last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)
	
	def __unicode__(self):
		return str(self.field)
	
	
