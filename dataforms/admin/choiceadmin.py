from dataforms.app_settings import ADMIN_JS
from django.contrib import admin


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'value',)
    search_fields = ('title','value')
    save_as = True
    
    
class ChoiceMappingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'field', 'choice', 'order',)
    list_filter = ('field',)
    list_editable = ('order',)
    
    def queryset(self, request):
        qs = super(ChoiceMappingAdmin, self).queryset(request)
        return qs.select_related('field', 'choice')
    
    class Media:
        js = ADMIN_JS

