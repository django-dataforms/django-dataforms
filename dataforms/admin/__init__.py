from answeradmin import AnswerAdmin, SubmissionAdmin
from bindingadmin import BindingAdmin
from choiceadmin import ChoiceAdmin, ChoiceMappingAdmin
from collectionadmin import SectionAdmin, CollectionAdmin, \
    CollectionMappingAdmin, CollectionVersionAdmin
from dataformadmin import DataFormAdmin
from fieldadmin import FieldMappingAdmin, FieldAdmin
from dataforms.models import Collection, CollectionDataForm, CollectionVersion, \
    DataForm, DataFormField, Field, Binding, FieldChoice, Choice, Answer, Submission, \
    Section, AnswerChoice
from dataforms.settings import ADMIN_JS
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.forms.models import ModelChoiceField
from forms import BindingAdminForm, FieldAdminForm
from inlines import ChoiceInline, CollectionInline, FieldInline


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





