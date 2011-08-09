from dataforms.models import Collection, CollectionDataForm, CollectionVersion, \
    DataForm, DataFormField, Field, Binding, FieldChoice, Choice, Answer, Submission, \
    Section
from dataforms.settings import ADMIN_JS
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseAdminClass
from django.forms.models import ModelChoiceField
from forms import BindingAdminForm, FieldAdminForm
from views import answers, ajax_filter
    

#try:
#    from reversion.admin import VersionAdmin as BaseAdminClass
#except ImportError:


#------------ Inline Model Admins that are attached ------ ----------------#

class CollectionInline(admin.TabularInline):
    model = CollectionDataForm
    extra = 0
    

class ChoiceInline(admin.TabularInline):
    model = FieldChoice
    extra = 1

class FieldInline(admin.TabularInline):
    model = DataFormField
    extra = 1


#------------------------ Main Model Admins classes -----------------------#

class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')
    inlines = [CollectionInline,]
    list_display = ('title', 'slug')
    save_as = True
    
    fieldsets = (
        (None, {
            'fields' : ('title', 'description', 'slug', 'visible',),
            'description': "Collections hold one or more Data Forms."
        }),
    )
    

class CollectionVersionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'collection', 'last_modified' )
    save_as = True
    
    
class CollectionMappingAdmin(admin.ModelAdmin):
    list_display = ('collection', 'data_form', 'section', 'order',)
    list_filter = ('collection__title', 'section__title',)
    list_editable = ('order',)

    def collection_title(self, obj):
        return obj.collection.title

    def dataform_title(self, obj):
        return obj.data_form.title

    def section_title(self, obj):
        return obj.section.title
    
    class Media:
        js = ADMIN_JS
    
    
class DataFormAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', '__unicode__', 'visible', 'properties_link', 'fields_link', 'bindings_link')
    list_display_links = ('pk',)
    list_filter = ('collection__title', 'collectiondataform__section__title')
    list_select_related = True

    search_fields = ('title', 'slug')
    inlines = [CollectionInline, FieldInline]
    save_as = True
    filter_horizontal = ('fields',)
    
    fieldsets = (
        (None, {
            'fields' : ('title', 'description', 'slug', 'visible',),
            'description': "A data form is a dynamic Django form."
        }),
    )
    
    def properties_link(self, obj):
        return '<a href="%s">Properties<a>' % obj.pk
    properties_link.allow_tags = True
    properties_link.short_description = "Properties"

    def fields_link(self, obj):
        return '<a href="../dataformfield/?data_form__id__exact=%s">Fields<a>' % obj.pk
    fields_link.allow_tags = True
    fields_link.short_description = "Fields"

    def bindings_link(self, obj):
        return '<a href="../binding/?data_form__title=%s">Bindings<a>' % obj.title
    bindings_link.allow_tags = True
    bindings_link.short_description = "Bindings"
    

class FieldMappingAdmin(admin.ModelAdmin):
    list_display = ('data_form', 'field', 'field_label', 'order')
    list_filter = ('data_form',)
    list_editable = ('order',)
    search_fields = ('data_form__title', 'field__slug', 'field__label')

    def field_label(self, obj):
        return obj.field.label
        
    class Media:
        js = ADMIN_JS
        
class FieldAdmin(admin.ModelAdmin):
    list_select_related = True
    list_filter = ('dataform__title', 'field_type', 'visible', 'required',)
    list_display_links = ('label',)
    list_display = ('label', 'slug', 'field_type', 'visible', 'required', 'choices_link')
    list_editable = ('field_type', 'visible', 'required',)
    search_fields = ('label','slug')
    inlines = [ChoiceInline, FieldInline]
    save_as = True
    form = FieldAdminForm
    
    def choices_link(self, obj):
        return '<a href="../fieldchoice/?field__id__exact=%s">Choices<a>' % obj.pk
    choices_link.allow_tags = True
    choices_link.short_description = "Choices"
    

class BindingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data_form', 'field', 'operator', 'value', 
                    'field_choice', 'true_fields_list', 'false_fields_list')
    list_filter = ('data_form__title',)
    list_select_related = True
    search_fields = ('data_form__title', 'field__slug')
    save_as = True
    
    form = BindingAdminForm
    
    def true_fields_list(self, obj):
        fields = ''.join([
            '<li>' + c + '</li>' for c in obj.true_field
        ]) if obj.true_field else ''
        choices = ''.join([
            '<li>' + '%s (%s)' % (c.split('___')[0], c.split('___')[1].upper()) + '</li>' 
            for c in obj.true_choice
        ]) if obj.true_choice else ''
        return '<ul>' + fields + choices + '</ul>'
    true_fields_list.allow_tags = True


    def false_fields_list(self, obj):
        fields = ''.join([
            '<li>' + c + '</li>' for c in obj.false_field
        ]) if obj.false_field else ''
        choices = ''.join([
            '<li>' + '%s (%s)' % (c.split('___')[0], c.split('___')[1].upper()) + '</li>'
            for c in obj.false_choice
        ]) if obj.false_choice else ''
        return '<ul>' + fields + choices + '</ul>'
    false_fields_list.allow_tags = True
    

    def get_urls(self):
        urls = super(BindingAdmin, self).get_urls()
        new_urls = patterns('',
            (r'ajax/(?P<object>(dataformfield|fieldchoice))/$', 
             self.admin_site.admin_view(ajax_filter, cacheable=True)),
        )
        return new_urls + urls
    
    
    class Media:
        js = ADMIN_JS


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'value',)
    search_fields = ('title','value')
    save_as = True
    
    
class ChoiceMappingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'field', 'choice', 'order',)
    list_filter = ('field',)
    list_editable = ('order',)
    
    class Media:
        js = ADMIN_JS


class SectionAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'title', 'slug',)
    list_filter = ('collectiondataform__collection__title',)
    search_fields = ('title','slug')
    save_as = True


class SubmissionAdmin(BaseAdminClass):
    list_display = ('id', '__unicode__', 'last_modified', 'answers_link')
    search_fields = ('slug',)
    list_select_related = True
    
    def answers_link(self, obj):
        return '<a href="answers/%s/">Answers<a>' % obj.pk
    answers_link.allow_tags = True
    answers_link.short_description = "Fields"
    
    def get_urls(self):
        urls = super(SubmissionAdmin, self).get_urls()
        new_urls = patterns('',
            (r'answers/(?P<submissionid>\d+)/$', 
             self.admin_site.admin_view(answers, cacheable=True)),
        )
        return new_urls + urls
    
    
#------------ Model Admins that are hidden from view ----------------#

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'data_form', 'field', 'field_type', 'value', 'choices')
    #inlines = [AnswerTextInline, AnswerNumberInline, AnswerChoiceInline]
    list_select_related = True
    
    search_fields = ('field__slug', 'field__label')
    
    # Get Choices
    def choices(self, obj):
        return '%s' % obj.choice.all()

    # Get Field Types
    def field_type(self, obj):
        return '%s' % obj.field.field_type
    
    #Hide the model from view
#    def get_model_perms(self, request):
#        return {}
    
    
admin.site.register(Section, SectionAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionDataForm, CollectionMappingAdmin)
admin.site.register(CollectionVersion, CollectionVersionAdmin)
admin.site.register(DataForm, DataFormAdmin)
admin.site.register(DataFormField, FieldMappingAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Binding, BindingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(FieldChoice, ChoiceMappingAdmin)





