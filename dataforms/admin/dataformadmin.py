from dataforms.app_settings import ADMIN_JS, ADMIN_CSS
from django.contrib import admin
from inlines import CollectionInline, FieldInline


class DataFormAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'visible', 'fields_link', 'bindings_link')
    #list_display_links = ('pk',)
    list_filter = ('collection__title', 'collectiondataform__section__title')
    list_select_related = True

    search_fields = ('title', 'slug')
    #inlines = [CollectionInline, FieldInline]
    inlines = [FieldInline]
    save_as = True
    filter_horizontal = ('fields',)
    
    fieldsets = (
        ('Form Information', {
            'fields' : ('title', 'description', 'slug', 'javascript_include', 'visible',),
        }),
    )
    
    def fields_link(self, obj):
        return '<a href="../dataformfield/?data_form__id__exact=%s">Fields<a>' % obj.pk
    fields_link.allow_tags = True
    fields_link.short_description = "Fields"

    def bindings_link(self, obj):
        return '<a href="../binding/?data_form__slug=%s">Bindings<a>' % obj.slug
    bindings_link.allow_tags = True
    bindings_link.short_description = "Bindings"
    
    class Media:
        js = ADMIN_JS
        css = { 'all' : ADMIN_CSS }