from django import forms
from django.contrib import admin

try:
	from reversion.admin import VersionAdmin as BaseAdminClass
except ImportError:
	from django.contrib.admin import ModelAdmin as BaseAdminClass

from .settings import ADMIN_SORT_JS
from .models import (Collection, CollectionDataForm, CollectionVersion, DataForm, DataFormField,
					 Field, Binding, FieldChoice, Choice, Answer, Submission,
					 AnswerText, AnswerChoice, AnswerNumber, Section, ParentField,
					 ParentFieldChoice, ChildField)

# Admin Forms
class FieldAdminForm(forms.ModelForm):
	class Meta:
		model = Field
		
	def clean_label(self):
		data = self.cleaned_data['label']

		if 'meta' in data:
			raise forms.ValidationError("You cannot use the term 'meta' as a label as it is reserved.")
		return data

# Inline ModelAdmin classes
class DataFormInline(admin.StackedInline):
	model = CollectionDataForm
	extra = 1

class ChoiceInline(admin.StackedInline):
	model = FieldChoice
	extra = 1

class FieldInline(admin.StackedInline):
	model = DataFormField
	extra = 1

class BindingInline(admin.StackedInline):
	model = Binding
	extra = 1
	
class ParentFieldInline(admin.StackedInline):
	model = ParentField
	extra = 1
	
class ParentFieldChoiceInline(admin.StackedInline):
	model = ParentFieldChoice
	extra = 1
	
class ChildFieldInline(admin.StackedInline):
	model = ChildField
	extra = 1
	
class AnswerChoiceInline(admin.StackedInline):
	model = AnswerChoice
	extra = 1
class AnswerTextInline(admin.StackedInline):
	model = AnswerText
	extra = 1
class AnswerNumberInline(admin.StackedInline):
	model = AnswerNumber
	extra = 1

# ModelAdmin Classes
class CollectionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	inlines = [DataFormInline,]
	list_display = ('title', 'slug')
	save_as = True
	
	class Media:
		js = ADMIN_SORT_JS

class CollectionVersionAdmin(admin.ModelAdmin):
	list_display = ('slug', 'collection', 'last_modified' )
	save_as = True

class DataFormAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('__unicode__', 'visible',)
	inlines = [FieldInline]
	save_as = True
	
	class Media:
		js = ADMIN_SORT_JS

class FieldAdmin(admin.ModelAdmin):
	list_select_related = True
	list_filter = ('field_type', 'visible', 'required',)
	list_display_links = ('label',)
	list_display = ('label', 'slug', 'field_type', 'visible', 'required',)
	list_editable = ('field_type', 'visible', 'required')
	search_fields = ('label','slug')
	inlines = [ChoiceInline, FieldInline]
	save_as = True
	form = FieldAdminForm
	
	class Media:
		js = ADMIN_SORT_JS
		
class BindingAdmin(admin.ModelAdmin):
	list_display = ('data_form',)
	inlines = [ParentFieldInline, ParentFieldChoiceInline, ChildFieldInline]
	save_as = True
	
	class Media:
		js = ADMIN_SORT_JS
		
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('id', 'submission', 'data_form', 'field', )
	inlines = [AnswerTextInline, AnswerNumberInline, AnswerChoiceInline]
	list_select_related = True
	search_fields = ('field__slug', 'field__label')

class AnswerChoiceAdmin(BaseAdminClass):
	list_display = ('id', 'answer', 'choice')
	search_fields = ('answer__field__slug', 'answer__field__label')

class AnswerTextAdmin(BaseAdminClass):
	list_display = ('id', 'answer', 'text')
	search_fields = ('answer__field__slug', 'answer__field__label')

class AnswerNumberAdmin(BaseAdminClass):
	list_display = ('id', 'answer', 'num')
	search_fields = ('answer__field__slug', 'answer__field__label')

class SubmissionAdmin(BaseAdminClass):
	list_display = ('id', '__unicode__', 'last_modified',)
	search_fields = ('slug',)
	list_select_related = True

class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('title', 'value',)
	search_fields = ('title','value')
	save_as = True

class SectionAdmin(admin.ModelAdmin):
	list_display = ('title',)
	save_as = True
	
admin.site.register(Section, SectionAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionVersion, CollectionVersionAdmin)
admin.site.register(DataForm, DataFormAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Binding, BindingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)
admin.site.register(AnswerText, AnswerTextAdmin)
admin.site.register(AnswerNumber, AnswerNumberAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Choice, ChoiceAdmin)
