from validators import reserved_delimiter
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CommaSeparatedIntegerField
from django.utils.translation import ugettext_lazy as _
from fields import SeparatedValuesField
from app_settings import FIELD_TYPE_CHOICES, BINDING_OPERATOR_CHOICES, \
    BINDING_ACTION_CHOICES
    

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
    section = models.ForeignKey('Section', blank=True, null=True)
    order = models.IntegerField(verbose_name=_('order'), blank=True, null=True)

    class Meta:
        unique_together = ('collection', 'data_form', 'section')
        ordering = ['order', ]
        verbose_name = 'Collection Mapping'
        verbose_name_plural = 'Collection Mappings'

    def __unicode__(self):
        return u'%s in %s (%s)' % (self.collection, self.data_form, self.section)


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
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True, validators=[reserved_delimiter])
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
    field_type = models.CharField(verbose_name=_('field type key'),
        max_length=255, choices=FIELD_TYPE_CHOICES)
    label = models.TextField(verbose_name=_('field label'))
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True, validators=[reserved_delimiter])
    help_text = models.TextField(verbose_name=_('field help text'), blank=True)
    initial = models.TextField(verbose_name=_('initial value of the field'), blank=True)
    classes = models.CharField(verbose_name=_('additional widget classes'), 
                                      help_text="A comma separated string of class names.", blank=True, max_length=255)
    arguments = models.CharField(verbose_name=_('additional field arguments'),
        help_text="A JSON dictionary of keyword arguments.", blank=True, max_length=255)
    required = models.BooleanField(verbose_name=_('field is required'), default=False)
    visible = models.BooleanField(verbose_name=_('field is visible'), default=True)

    def __unicode__(self):
        return self.slug
    
    class Meta:
        ordering = ['slug', ]


class Binding(models.Model):
    data_form = models.ForeignKey('DataForm')
    field = models.ForeignKey('Field')
    field_choice = models.ForeignKey('FieldChoice', blank=True, null=True,
        help_text='Optionally narrow down to a choice on this field if available.')
    operator = models.CharField(max_length=255, choices=BINDING_OPERATOR_CHOICES)
    value = models.CharField(max_length=255, blank=True,
        help_text="Required if a Operator is equal to 'checked'.")
    
    true_field = SeparatedValuesField(blank=True)
    true_choice = SeparatedValuesField(blank=True)

    false_field = SeparatedValuesField(blank=True)
    false_choice = SeparatedValuesField(blank=True)

    action = models.CharField(max_length=255, choices=BINDING_ACTION_CHOICES, default='show-hide')
    function = models.CharField(max_length=255, blank=True,
        help_text="Required if Action is equal to 'Function'.")
    
    additional_rules = CommaSeparatedIntegerField(max_length=200, blank=True)
    
    def clean(self):
        # Field requires a Operator and Value
        if self.operator != 'checked' and not self.value:
            raise ValidationError("A Value is required if the Operator is not equal to 'checked'.")

        if self.field_choice and self.operator != 'checked':
            raise ValidationError("Operator must be equal to 'checked of Field Choice is selected.")
        
        # A field or choice is required
        if (not self.true_field and not self.true_choice
            and not self.false_field and not self.field_choice):
            raise ValidationError('A Field or Choice is required.')

        # If action is function, then a function is needed
        if self.action == 'function' and not self.function:
            raise ValidationError('A function is required if action is function.')
        
        # If additional rules are applied, then the rules cannot be the same as current record
        if self.additional_rules and unicode(self.id) in self.additional_rules:
            raise ValidationError('You cannot apply the current rule to additional rules.')
        
    
    def __unicode__(self):
        return '%s' % self.pk
 
    
class FieldChoiceManager(models.Manager):

    def get_fieldchoice_data(self):
    
        sql = '''
            SELECT fc.id, fc.choice_id, fc.field_id, f.slug AS field_slug, 
                d.slug AS data_form_slug, c.value AS choice_value
            FROM dataforms_fieldchoice fc 
            INNER JOIN dataforms_field f ON f.id = fc.field_id
            INNER JOIN dataforms_choice c ON c.id = fc.choice_id
            INNER JOIN dataforms_dataformfield df ON df.field_id = f.id
            INNER JOIN dataforms_dataform d ON d.id = df.data_form_id
            
            ORDER BY d.slug
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
    title = models.CharField(verbose_name=_('choice title'), max_length=255, unique=True)
    value = models.CharField(verbose_name=_('choice value'), max_length=255, validators=[reserved_delimiter])

    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        ordering = ['title']
        # FIXME: This fails on MySQL using InnoDB due to MySQL bug http://bugs.mysql.com/bug.php?id=4541
        #unique_together = ('title', 'value',)


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
            SELECT a.*, f.field_type, f.slug AS field_slug, 
                d.slug AS data_form_slug, c.value as choice_value, ac.choice_id
                     FROM dataforms_answer a 
                     LEFT JOIN dataforms_answerchoice ac ON a.id = ac.answer_id
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
            sql += 'AND f.slug IN (%s)' % ','.join(["%s"]*len(field_slugs))
            params += field_slugs

        return self.raw(sql, tuple(params))


class Answer(models.Model):
    """
    Model that holds answers for each submission
    """

    submission = models.ForeignKey(Submission)
    data_form = models.ForeignKey(DataForm)
    field = models.ForeignKey(Field)
    value = models.TextField(blank=True, null=True)
    choice = models.ManyToManyField(Choice, through='AnswerChoice', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.field)

    objects = AnswerManager()


class AnswerChoice(models.Model):
    choice = models.ForeignKey('Choice')
    answer = models.ForeignKey('Answer')
    
    def __unicode__(self):
        return self.choice.title

