from dataforms.app_settings import ADMIN_JS
from django.contrib import admin
from inlines import CollectionInline, FieldInline


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
    
    class Media:
        js = ADMIN_JS