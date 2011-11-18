from dataforms.admin.forms import BindingAdminForm
from dataforms.app_settings import ADMIN_JS
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from django.utils import simplejson


def ajax_filter(request, object):
    
    #Return 404 if not an ajax request
    if not request.is_ajax():
        raise Http404
    
    values = []
    order = []
    filter = {}
    
    if request.GET.has_key('values'):
        values = request.GET['values'].split(',')
    
    if request.GET.has_key('order'):
        order = request.GET['order'].split(',')

    for key, value in request.GET.iteritems():
        if key != 'order' and key !='values':
            filter[str(key)] = str(value)
    
    try:    
        model_class = ContentType.objects.get(app_label="dataforms", model=object).model_class()
        queryset = model_class.objects.values(*values).order_by(*order).filter(**filter)
    
    except:
        return JsonResponse(0)
        
    return JsonResponse(list(queryset))
    

class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


class BindingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data_form', 'field', 'operator', 'value',
                    'field_choice', 'true_fields_list', 'false_fields_list')
    list_filter = ('data_form__slug',)
    list_select_related = True
    search_fields = ('data_form__title', 'field__slug')
    save_as = True
    
    form = BindingAdminForm
    
    def queryset(self, request):
        qs = super(BindingAdmin, self).queryset(request)
        return qs.select_related('data_form', 'field', 'field_choice__choice', 'field_choice__field')
    
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
        

