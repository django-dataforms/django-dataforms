from dataforms.models import CollectionDataForm, FieldChoice, DataFormField
from django.contrib import admin


class CollectionInline(admin.TabularInline):
    model = CollectionDataForm
    extra = 0
    

class ChoiceInline(admin.TabularInline):
    model = FieldChoice
    extra = 1


class FieldInline(admin.TabularInline):
    model = DataFormField
    extra = 1