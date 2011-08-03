from django.core.exceptions import ValidationError
from django.db import models, connection, connections
from django.db.models.fields import CommaSeparatedIntegerField
from django.utils.translation import ugettext_lazy as _
from fields import SeparatedValuesField
from itertools import izip
from settings import FIELD_TYPE_CHOICES, BINDING_OPERATOR_CHOICES, \
    BINDING_ACTION_CHOICES
from utils.sql import query_to_grouped_dict

    

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


class BindingManager(models.Manager):
    
    def get_binding_data(self, data_form_id, using="default"):
        
        cursor = connections[using].cursor()
        
        # When you need many to many, use raw()....its awesome!
        sql = '''
            SELECT b.id, b.data_form_id, b.field_id, b.field_choice_id, b.operator, b.action, b.function, b.value,
                   f.slug AS field_slug, ffc.slug AS fieldchoice_slug, ffcc.value AS fieldchoice_value,
                   btff.slug AS true_fields, bfff.slug AS false_fields, 
                   (btccf.slug || '___' || btccc.value) AS true_choices, 
                   (bfccf.slug || '___' || bfccc.value) AS false_choices
                    
                    FROM dataforms_binding b
                    INNER JOIN dataforms_dataform d ON b.data_form_id = d.id
                    LEFT JOIN dataforms_field f ON b.field_id = f.id
                    LEFT JOIN dataforms_fieldchoice fc ON b.field_choice_id = fc.id
                    LEFT JOIN dataforms_field ffc ON fc.field_id = ffc.id
                    LEFT JOIN dataforms_choice ffcc ON fc.choice_id = ffcc.id
                    
                    LEFT JOIN dataforms_binding_true_field AS btf ON b.id = btf.binding_id
                    LEFT JOIN dataforms_field AS btff ON btf.field_id = btff.id
                    
                    
                    LEFT JOIN dataforms_binding_false_field AS bff ON b.id = bff.binding_id
                    LEFT JOIN dataforms_field AS bfff ON bff.field_id = bfff.id
                    
                    
                    LEFT JOIN dataforms_binding_true_choice AS btc ON b.id = btc.binding_id
                    LEFT JOIN dataforms_fieldchoice AS btcc ON btc.fieldchoice_id = btcc.id
                    LEFT JOIN dataforms_field AS btccf ON btcc.field_id = btccf.id
                    LEFT JOIN dataforms_choice AS btccc ON btcc.choice_id = btccc.id
                    
                    
                    LEFT JOIN dataforms_binding_false_choice AS bfc ON b.id = bfc.binding_id
                    LEFT JOIN dataforms_fieldchoice AS bfcc ON bfc.fieldchoice_id = bfcc.id
                    LEFT JOIN dataforms_field AS bfccf ON bfcc.field_id = bfccf.id
                    LEFT JOIN dataforms_choice AS bfccc ON bfcc.choice_id = bfccc.id
            
            WHERE d.id = %s
        '''
        
        params = [data_form_id]
        result = cursor.execute(sql, params)
        
        return query_to_grouped_dict(result)
       

class Binding(models.Model):
    data_form = models.ForeignKey('DataForm')
    field = models.ForeignKey('Field', blank=True, null=True, help_text='Please select either a Field or a Field choice')
    field_choice = models.ForeignKey('FieldChoice', blank=True, null=True)
    operator = models.CharField(max_length=255, choices=BINDING_OPERATOR_CHOICES, blank=True, help_text="Required if a Field is selected.")
    value = models.CharField(max_length=255, blank=True, help_text="Required if a Field is selected.")
    parent = models.CharField(max_length=255, blank=True, help_text="A parent selector that contains the True and False fields.")
    
    true_field = SeparatedValuesField(blank=True)
    true_choice = SeparatedValuesField(blank=True)

    false_field = SeparatedValuesField(blank=True)
    false_choice = SeparatedValuesField(blank=True)

    action = models.CharField(max_length=255, choices=BINDING_ACTION_CHOICES, default='show-hide')
    function = models.CharField(max_length=255, blank=True, help_text="Required if Action is 'Function'.")
    
    additional_rules = CommaSeparatedIntegerField(max_length=200, blank=True)
    
    objects = BindingManager()
    
    def clean(self):
        # Only Field or Field Choice should be selected
        if ((not self.field and not self.field_choice) or
            (self.field and self.field_choice)):
            raise ValidationError('A Field or Field Choice is required.')
        
        # Field required a Operator and Value
        if self.field and not self.value and self.operator != 'checked':
            raise ValidationError('A Operator and Value are required if a Field is selected' 
                                  ' and Operator is something other then defined as checked.')
        
        # A True Field or True Choice is required
        if not self.true_field and not self.true_choice:
            raise ValidationError('A True Field or True Choice is required.')

        # A False Field or False Choice is required
        if not self.false_field and not self.false_choice:
            raise ValidationError('A False Field or False Choice is required.')
        
        # If action is function, then a function is needed
        if self.action == 'function' and not self.function:
            raise ValidationError('A function is required if action is function.')
        
        # If additional rules are applied, then the rules cannot be the same as current record
        if self.additional_rules and unicode(self.id) in self.additional_rules:
            raise ValidationError('You cannot apply the current rule to additional rules.')
        
    
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
class FieldChoiceManager(models.Manager):

    def get_fieldchoice_data(self):
    
        sql = '''
            SELECT fc.id, fc.choice_id, fc.field_id, f.slug AS field_slug, d.slug AS data_form_slug, c.value AS choice_value
            FROM dataforms_fieldchoice fc 
            INNER JOIN dataforms_field f ON f.id = fc.field_id
            INNER JOIN dataforms_choice c ON c.id = fc.choice_id
            INNER JOIN dataforms_dataformfield df ON df.field_id = f.id
            INNER JOIN dataforms_dataform d ON d.id = df.data_form_id
        '''
        
        return self.raw(sql, [])


class FieldChoice(models.Model):
    """ 
    Model bridge for Field and Choice
    """

    # FIXME: Why are these nullable?
    field = models.ForeignKey('Field', null=True)
    choice = models.ForeignKey('Choice', null=True)
    order = models.IntegerField(verbose_name=_('order'), null=True, blank=True)

    objects = FieldChoiceManager()

    class Meta:
        unique_together = ('field', 'choice')
        ordering = ['field', 'order']
        verbose_name = 'Choice Mapping'
        verbose_name_plural = 'Choice Mappings'

    def __unicode__(self):
        return u'%s (%s)' % (self.field, self.choice)


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



    
    