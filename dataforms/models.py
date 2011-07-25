from django.core.exceptions import ValidationError
from django.db import models, connection, connections
from django.utils.translation import ugettext_lazy as _
from itertools import izip
from settings import FIELD_TYPE_CHOICES
from utils import cache_delete_by_tags


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
        return self.slug


class CollectionDataForm(models.Model):
    """ 
    Model bridge for Collection and DataForm
    """

    collection = models.ForeignKey('Collection', null=True)
    data_form = models.ForeignKey('DataForm', null=True)
    section = models.ForeignKey('Section', null=True)
    order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

    class Meta:
        unique_together = ('collection', 'data_form')
        ordering = ['order', ]
        verbose_name = 'Collection Mapping'
        verbose_name_plural = 'Collection Mappings'

    def __unicode__(self):
        return u'%s in %s' % (self.collection, self.data_form)


class CollectionVersion(models.Model):
    """
    Model that will keep a record of the newest version of a collection
    """
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
    collection = models.ForeignKey('Collection')
    last_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.slug, self.collection)


class Section(models.Model):
    """
    Model that gives a section to a DataForm within a Collection
    """
    title = models.CharField(verbose_name=_('section'), max_length=255, null=False, blank=False)
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)

    def __unicode__(self):
        return self.slug
    
    class Meta:
        ordering = ['title', ]


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
        return self.slug
    
    class Meta:
        ordering = ['title', ]


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
        verbose_name = 'Field Mapping'
        verbose_name_plural = 'Field Mappings'

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
    
    class Meta:
        ordering = ['slug', ]

OPERATOR_CHOICES = (
    ('equal', 'Equal',),
    ('not-equal', 'Not Equal',),
    ('checked', 'Checked',),
    ('contains', 'Contains',),
    ("doesn't contain", "Doesn't Contain",),
)

ACTION_CHOICES = (
    ('show', 'Show',),
    ('hide', 'hide',),
    ('function', 'Custom Function',),
)

class Condition(models.Model):
    data_form = models.ForeignKey('DataForm')
    field = models.ForeignKey('Field')
    operator = models.CharField(max_length=255, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=255)
    
    true_field = models.ManyToManyField('Field', related_name='true_field_set', blank=True, null=True)
    true_choice = models.ManyToManyField('FieldChoice', related_name='true_choice_set', blank=True, null=True)

    false_field = models.ManyToManyField('Field', related_name='false_field_set', blank=True, null=True)
    false_choice = models.ManyToManyField('FieldChoice', related_name='false_choice_set', blank=True, null=True)
    
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    function = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return '%s' % self.pk
    

#class Binding(models.Model):
#    data_form = models.ForeignKey('DataForm', null=False, blank=False)
#    parent_fields = models.ManyToManyField('Field', related_name='fields_set', through='ParentField')
#    parent_choices = models.ManyToManyField('FieldChoice', related_name='choices_set', through='ParentFieldChoice')
#    children = models.ManyToManyField('Field', through='ChildField')
#    
#    def save(self, *args, **kwargs):
#        cache_delete_by_tags(['dataforms_bindings'])
#        super(Binding, self).save(*args, **kwargs)
#    
#    def delete(self):
#        cache_delete_by_tags(['dataforms_bindings'])
#        super(Binding, self).delete()
#    
#    def __unicode__(self):
#        return '%s' % self.pk
#
#
#class ParentField(models.Model):
#    binding = models.ForeignKey('Binding')
#    parent_field = models.ForeignKey('Field', help_text="Leave blank if a choice is selected", null=False, blank=False)
#    
#    
#class ParentFieldChoice(models.Model):
#    binding = models.ForeignKey('Binding')
#    field_choice = models.ForeignKey('FieldChoice', help_text="Leave blank if a parent is selected", null=False, blank=False)
#    
#    
#class ChildField(models.Model):
#    binding = models.ForeignKey('Binding')
#    field = models.ForeignKey('Field', null=False, blank=False)


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
        ordering = ['field', 'order']
        verbose_name = 'Choice Mapping'
        verbose_name_plural = 'Choice Mappings'

    def __unicode__(self):
        return u'%s (%s)' % (self.field, unicode(self.choice).upper())


class Choice(models.Model):
    """
    Model that holds choices for fields and their values
    """
    title = models.CharField(verbose_name=_('choice title'), max_length=255)
    value = models.CharField(verbose_name=_('choice value'), max_length=255)

    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        ordering = ['title']
        unique_together = ('title', 'value',)


class Submission(models.Model):
    """
    Model that holds a unique submission
    """
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)
    collection = models.ForeignKey('Collection', null=True, blank=True)
    last_modified = models.DateTimeField(verbose_name=_('last modified'), auto_now=True)

    def __unicode__(self):
        return unicode(self.slug)


class AnswerManager(models.Manager):

    def get_answer_data(self, submission_id, field_slugs=None, data_form_id=None):
        
        # When you need many to many, use raw()....its awesome!
        sql = '''
            SELECT a.*, f.slug AS field_slug, d.slug AS data_form_slug, c.value as choice_value, ac.choice_id
                     FROM dataforms_answer a 
                     LEFT JOIN dataforms_answer_choice ac ON a.id = ac.answer_id
                     LEFT JOIN dataforms_choice c ON ac.choice_id = c.id
                     INNER JOIN dataforms_field f ON a.field_id = f.id
                     INNER JOIN dataforms_dataform d ON a.data_form_id = d.id 
            WHERE a.submission_id = %s
        '''
        
        params = [submission_id]
        
        if data_form_id:
            sql += 'AND a.data_form_id = %s '
            params.append(data_form_id)
            
        if field_slugs:
            sql += 'AND a.field_id IN (%s)'
            params.append(','.join(field_slugs))
        
        return self.raw(sql, params)


class Answer(models.Model):
    """
    Model that holds answers for each submission
    """

    submission = models.ForeignKey(Submission)
    data_form = models.ForeignKey(DataForm)
    field = models.ForeignKey(Field)
    value = models.TextField(blank=True, null=True)
    choice = models.ManyToManyField(Choice, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.field)

    objects = AnswerManager()


def insert_many(objects, using="default"):
    """Insert list of Django objects in one SQL query. Objects must be
    of the same Django model. Note that save is not called and signals
    on the model are not raised."""
    if not objects:
        return

    con = connections[using]
    
    model = objects[0].__class__
    fields = [f for f in model._meta.fields if not isinstance(f, models.AutoField)]
    parameters = []
    for o in objects:
        parameters.append(tuple(f.get_db_prep_save(f.pre_save(o, True), connection=con) for f in fields))

    table = model._meta.db_table
    column_names = ",".join(con.ops.quote_name(f.column) for f in fields)
    placeholders = ",".join(("%s",) * len(fields))
    con.cursor().executemany(
        "insert into %s (%s) values (%s)" % (table, column_names, placeholders),
        parameters)


def update_many(objects, fields=[], using="default"):
    """Update list of Django objects in one SQL query, optionally only
    overwrite the given fields (as names, e.g. fields=["foo"]).
    Objects must be of the same Django model. Note that save is not
    called and signals on the model are not raised."""
    if not objects:
        return

    con = connections[using]

    names = fields
    meta = objects[0]._meta
    fields = [f for f in meta.fields if not isinstance(f, models.AutoField) and (not names or f.name in names)]

    if not fields:
        raise ValueError("No fields to update, field names are %s." % names)
    
    fields_with_pk = fields + [meta.pk]
    parameters = []
    for o in objects:
        parameters.append(tuple(f.get_db_prep_save(f.pre_save(o, True), connection=con) for f in fields_with_pk))

    table = meta.db_table
    assignments = ",".join(("%s=%%s" % con.ops.quote_name(f.column)) for f in fields)
    con.cursor().executemany(
        "update %s set %s where %s=%%s" % (table, assignments, con.ops.quote_name(meta.pk.column)),
        parameters)
    
    
def delete_many(objects, table=None, using="default"):
    
    con = connections[using]
    
    fields = [(o.id,) for o in objects]   
    meta = objects[0]._meta
    
    parameters = fields
    
    table = table or meta.db_table
    con.cursor().executemany(
        "delete from %s where %s=%%s" % (table, con.ops.quote_name(meta.pk.column)),
        parameters)
    
    
    