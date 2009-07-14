from django import forms
from django.contrib import admin

from .settings import ADMIN_SORT_JS
from .models import Collection, CollectionDataForm, DataForm, DataFormField, Field, Binding, FieldChoice, Choice, Answer, Submission, AnswerText, AnswerChoice, AnswerNumber

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
	
	class Media:
		js = ADMIN_SORT_JS

class DataFormAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('__unicode__', 'visible',)
	inlines = [FieldInline]
	
	class Media:
		js = ADMIN_SORT_JS

class FieldAdmin(admin.ModelAdmin):
	list_select_related = True
	list_filter = ('field_type', 'visible', 'required',)
	list_display_links = ('label',)
	list_display = ('label', 'field_type', 'visible', 'required',)
	list_editable = ('field_type', 'visible', 'required')
	search_fields = ('label',)
	inlines = [ChoiceInline, FieldInline]
	save_as = True
	form = FieldAdminForm
	
	class Media:
		js = ADMIN_SORT_JS
		
class BindingAdmin(admin.ModelAdmin):
	list_display = ('parent_field', 'parent_choice', 'child',)
		
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('submission', 'field', 'last_modified',)
	inlines = [AnswerTextInline, AnswerNumberInline, AnswerChoiceInline]
	list_select_related = True

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'last_modified',)
	search_fields = ('slug',)
	list_select_related = True

class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('title', 'value',)
	search_fields = ('text',)


admin.site.register(Collection, CollectionAdmin)
admin.site.register(DataForm, DataFormAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Binding, BindingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Choice, ChoiceAdmin)
