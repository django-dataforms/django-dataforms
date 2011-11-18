from dataforms.app_settings import ADMIN_JS
from django.contrib import admin
from inlines import CollectionInline


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
    
    class Media:
        js = ADMIN_JS


class CollectionMappingAdmin(admin.ModelAdmin):
    list_display = ('collection', 'data_form', 'section', 'order',)
    list_filter = ('collection__title', 'section__title',)
    list_editable = ('order',)
    list_select_related = True
    
    def queryset(self, request):
        qs = super(CollectionMappingAdmin, self).queryset(request)
        return qs.select_related('data_form', 'collection', 'section')
    
    def collection_title(self, obj):
        return obj.collection.title

    def dataform_title(self, obj):
        return obj.data_form.title

    def section_title(self, obj):
        return obj.section.title
    
    class Media:
        js = ADMIN_JS
        
        
class SectionAdmin(admin.ModelAdmin):
    list_display_links = ('pk',)
    list_display = ('pk', 'title', 'slug',)
    list_filter = ('collectiondataform__collection__title',)
    search_fields = ('title','slug')
    save_as = True