from models import DataFormCollection, DataFormCollectionDataForm, DataForm, DataFormField, Field, FieldChoice, Choice, Answer, Submission
from django import forms
from django.contrib import admin
from settings import ADMIN_SORT_JS

#Admin Forms
class FieldAdminForm(forms.ModelForm):
	class Meta:
		model = Field
		
	def clean_label(self):
		data = self.cleaned_data['label']

		if 'meta' in data:
			raise forms.ValidationError("You cannot use the term 'meta' as a label as it is reserved.")
		return data

#Inline ModelAdmin classes
class DataFormInline(admin.StackedInline):
	model = DataFormCollectionDataForm
	extra = 1

class ChoiceInline(admin.StackedInline):
	model = FieldChoice
	extra = 1

class FieldInline(admin.StackedInline):
	model = DataFormField
	extra = 1

#ModelAdmin Classes
class DataFormCollectionAdmin(admin.ModelAdmin):
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

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('submission', 'field', 'content', 'last_modified',)
	search_fields = ('content',)
	list_select_related = True

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'last_modified',)
	search_fields = ('slug',)
	list_select_related = True

class ChoiceAdmin(admin.ModelAdmin):
	list_display = ('title', 'value',)
	search_fields = ('text',)


admin.site.register(DataFormCollection, DataFormCollectionAdmin)
admin.site.register(DataForm, DataFormAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Choice, ChoiceAdmin)
